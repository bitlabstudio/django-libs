"""Custom admin command to clean up mailer's messagelog."""
from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta

from mailer.models import MessageLog


class Command(BaseCommand):
    def handle(self, **options):
        # Get logs older than 4 months
        old_logs = MessageLog.objects.filter(
            when_attempted__lt=now() - timedelta(days=122))
        if not old_logs:
            print('No message logs to delete.')
            return
        log_count = old_logs.count()
        old_logs.delete()
        print('Deleted {} message logs.'.format(log_count))
