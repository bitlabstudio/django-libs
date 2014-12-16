"""Utility functions for sending emails."""
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import force_text

import mailer

from .utils import html_to_plain_text


def send_email(request, extra_context, subject_template, body_template,
               from_email, recipients, priority="medium"):
    """
    Sends an email based on templates for subject and body.

    :param request: The current request instance.
    :param extra_context: A dictionary of items that should be added to the
        templates' contexts.
    :param subject_template: A string representing the path to the template of
        of the email's subject.
    :param body_template: A string representing the path to the template of
        the email's body.
    :param from_email: String that represents the sender of the email.
    :param recipients: A list of tuples of recipients. The tuples are similar
        to the ADMINS setting.

    """
    if request:
        context = RequestContext(request, extra_context)
    else:
        context = extra_context
    if request and request.get_host():
        context.update({'domain': '{}://{}'.format(
            'https' if request.is_secure() else 'http', request.get_host())})
    else:
        context.update({'domain': Site.objects.get_current().domain})
    subject = render_to_string(subject_template, context)
    subject = ''.join(subject.splitlines())
    message_html = render_to_string(body_template, context)
    message_plaintext = html_to_plain_text(message_html)
    if settings.EMAIL_BACKEND == 'mailer.backend.DbBackend':
        mailer.send_html_mail(subject, message_plaintext, message_html,
                              from_email, recipients, priority=priority)
    else:
        subject = force_text(subject)
        message = force_text(message_plaintext)

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipients,
            bcc=None,
            attachments=None,
            headers=None,
        )
        email = EmailMultiAlternatives(
            email.subject, email.body, email.from_email, email.to,
            headers=None)
        email.attach_alternative(message_html, "text/html")
        email.send()
