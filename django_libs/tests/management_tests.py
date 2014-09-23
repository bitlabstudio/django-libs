"""Tests for the management commands of the ``django_libs`` app."""
from django.core.management import call_command
from django.test import TestCase
from django.utils.timezone import now, timedelta

from mailer.models import MessageLog

from .factories import MessageLogFactory


class CleanupMailerMessagelogTestCase(TestCase):
    """Tests for the ``cleanup_mailer_messagelog`` management command."""
    longMessage = True

    def test_reminder(self):
        self.assertFalse(call_command('cleanup_mailer_messagelog'))
        self.assertEqual(MessageLog.objects.all().count(), 0)
        MessageLogFactory()
        self.assertFalse(call_command('cleanup_mailer_messagelog'))
        self.assertEqual(MessageLog.objects.all().count(), 1)
        MessageLogFactory(when_attempted=now() - timedelta(days=200))
        self.assertEqual(MessageLog.objects.all().count(), 2)
        self.assertFalse(call_command('cleanup_mailer_messagelog'))
        self.assertEqual(MessageLog.objects.all().count(), 1)
