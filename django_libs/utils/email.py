"""Utility functions for sending emails."""
import django
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_text

try:
    import mailer
except ImportError:  # pragma: nocover
    pass

from .converter import html_to_plain_text


def send_email(request, context, subject_template, body_template,
               from_email, recipients, priority="medium", reply_to=None,
               headers={}):
    """
    Sends an email based on templates for subject and body.

    :param request: The current request instance.
    :param context: A dictionary of items that should be added to the
        templates' contexts.
    :param subject_template: A string representing the path to the template of
        of the email's subject.
    :param body_template: A string representing the path to the template of
        the email's body.
    :param from_email: String that represents the sender of the email.
    :param recipients: A list of tuples of recipients. The tuples are similar
        to the ADMINS setting.
    :param priority: Sets the priority of the email (only used by django-mailer
        to prioritise email sendings).
    :param reply_to: Optional email address to reply to.
    :param headers: Additional dictionary to add header attributes.

    """
    if not reply_to:
        reply_to = from_email
    if django.get_version() >= '1.8':
        # The reply_to argument has been added in 1.8
        reply_to = [reply_to]
    else:
        headers.update({'Reply-To': reply_to})
    if request and request.get_host():
        domain = request.get_host()
        protocol = 'https://' if request.is_secure() else 'http://'
    else:
        domain = getattr(settings, 'DOMAIN', Site.objects.get_current().domain)
        protocol = getattr(settings, 'PROTOCOL', 'http://')
    context.update({
        'domain': domain,
        'protocol': protocol,
    })
    subject = render_to_string(template_name=subject_template,
                               context=context, request=request)
    subject = ''.join(subject.splitlines())
    message_html = render_to_string(template_name=body_template,
                                    context=context, request=request)
    message_plaintext = html_to_plain_text(message_html)
    if settings.EMAIL_BACKEND == 'mailer.backend.DbBackend':
        mailer.send_html_mail(
            subject, message_plaintext, message_html, from_email, recipients,
            priority=priority, headers=headers)
    else:
        subject = force_text(subject)
        message = force_text(message_plaintext)

        if django.get_version() >= '1.8':
            # The reply_to argument has been added in 1.8
            email = EmailMessage(
                subject=subject, body=message, from_email=from_email,
                to=recipients, headers=headers, reply_to=reply_to)
            email = EmailMultiAlternatives(
                email.subject, email.body, email.from_email, email.to,
                headers=email.extra_headers, reply_to=reply_to)
        else:
            email = EmailMessage(
                subject=subject, body=message, from_email=from_email,
                to=recipients, headers=headers)
            email = EmailMultiAlternatives(
                email.subject, email.body, email.from_email, email.to,
                headers=email.extra_headers)
        email.attach_alternative(message_html, "text/html")
        email.send()
