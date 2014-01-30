"""Tests for the email utils of ``django_libs``."""
from django.test import TestCase

from mailer.models import Message
from mock import Mock

from ..utils_email import send_email


class SendEmailTestCase(TestCase):
    """Tests for the ``send_email`` function."""
    longMessage = True

    def test_send_email(self):
        send_email(Mock(), {}, 'subject.html', 'html_email.html',
                   'info@example.com', ['recipient@example.com'])
        self.assertEqual(Message.objects.count(), 1, msg=(
            'An email should\'ve been sent'))
        send_email(None, {}, 'subject.html', 'html_email.html',
                   'info@example.com', ['recipient@example.com'])
        self.assertEqual(Message.objects.count(), 2, msg=(
            'An email should\'ve been sent'))
