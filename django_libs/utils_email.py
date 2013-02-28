"""Utility functions for sending emails."""
from django.template import RequestContext
from django.template.loader import render_to_string

from mailer import send_html_mail


def send_email(request, extra_context, subject_template, body_template_plain,
               body_template, from_email, recipients):
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
    subject = render_to_string(subject_template, context)
    subject = ''.join(subject.splitlines())
    message_plaintext = render_to_string(body_template_plain, context)
    message_html = render_to_string(body_template, context)
    send_html_mail(subject, message_plaintext, message_html, from_email,
                   recipients)
