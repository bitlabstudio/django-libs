"""Custom email backend for testing the project."""
import re

from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend
from django.core.mail.message import sanitize_address

from . import default_settings as settings


class EmailBackend(SmtpEmailBackend):
    """
    Email backend that sends all emails to a defined address, no matter what
    the recipient really is.

    In order to use it, set this in your local_settings.py::

        EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'
        TEST_EMAIL_BACKEND_RECIPIENTS = (
            ('Name', 'email@gmail.com'),
        )

    """
    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients() or \
                not settings.TEST_EMAIL_BACKEND_RECIPIENTS:
            return False
        from_email = sanitize_address(
            email_message.from_email, email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding)
                      for name, addr in settings.TEST_EMAIL_BACKEND_RECIPIENTS]
        try:
            self.connection.sendmail(
                from_email, recipients, email_message.message().as_string())
        except:
            if not self.fail_silently:
                raise
            return False
        return True


class WhitelistEmailBackend(SmtpEmailBackend):
    """
    Email backend that sends only these emails, that match the whitelist
    setting.

    In order to use it, set this in your local_settings.py::

        EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'
        EMAIL_BACKEND_WHITELIST = [
            r'.*@example\.com',
        ]

    This setting would allow all emails to @example.com to be sent and all
    others are discarded. The setting expects regex, so better test it before
    adding it here to prevent errors.

    If the setting does not exist, no emails are sent at all.

    """
    def _send(self, email_message):
        """A helper method that does the actual sending."""
        from_email = sanitize_address(
            email_message.from_email, email_message.encoding)
        recipients = self.clean_recipients(email_message)

        if not recipients:
            return False

        try:
            self.connection.sendmail(
                from_email, recipients, email_message.message().as_string())
        except:
            if not self.fail_silently:
                raise
            return False
        return True

    def clean_recipients(self, email_message):
        """Removes all the unallowed recipients."""
        new_recipients = []

        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]
        for recipient in recipients:
            if self.matches_whitelist(recipient):
                new_recipients.append(recipient)
            elif settings.EMAIL_BACKEND_REROUTE_BLACKLIST:
                for name, addr in settings.TEST_EMAIL_BACKEND_RECIPIENTS:
                    new_recipients.append(addr)
        # remove duplicates
        new_recipients = list(set(new_recipients))
        return new_recipients

    def matches_whitelist(self, recipient):
        """Checks if the email address matches one of the whitelist entries."""
        matches = False
        for entry in settings.EMAIL_BACKEND_WHITELIST:
            if re.match(entry, recipient):
                matches = True
        return matches
