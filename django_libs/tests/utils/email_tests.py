"""Tests for the email utils of ``django_libs``."""
from django.core import mail
from django.test import TestCase

from mailer.models import Message
from mixer.backend.django import mixer
from mock import Mock

from ...utils.email import send_email


def context_fn(request):
    return {
        'foo': 'bar',
    }


class SendEmailTestCase(TestCase):
    """Tests for the ``send_email`` function."""
    longMessage = True

    def test_send_email(self):
        mixer.blend('sites.Site')
        request = Mock()
        request.is_secure = Mock(return_value=True)
        request.get_host = Mock(return_value='example.com')
        send_email(request, {}, 'subject.html', 'html_email.html',
                   'info@example.com', ['recipient@example.com'])
        self.assertEqual(len(mail.outbox), 1, msg=(
            'An email should\'ve been sent'))
        send_email(None, {}, 'subject.html', 'html_email.html',
                   'info@example.com', ['recipient@example.com'])
        self.assertEqual(len(mail.outbox), 2, msg=(
            'An email should\'ve been sent'))

        with self.settings(EMAIL_BACKEND='mailer.backend.DbBackend'):
            send_email(None, {}, 'subject.html', 'html_email.html',
                       'info@example.com', ['recipient@example.com'])
            self.assertEqual(Message.objects.count(), 1, msg=(
                'An email should\'ve been sent'))

    def test_cc_and_bcc(self):
        send_email(
            None,
            {},
            'subject.html',
            'html_email.html',
            'info@example.com',
            ['recipient@example.com'],
            cc=['cc@example.com'],
            bcc=['bcc@example.com']
        )
        email = mail.outbox[0]
        self.assertEqual(['cc@example.com'], email.cc)
        self.assertEqual(['bcc@example.com'], email.bcc)
