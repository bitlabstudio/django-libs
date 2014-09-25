"""Logging related utilities."""
import logging

from django.conf import settings


class AddCurrentUser(logging.Filter):
    """
    Adds the current user to the log record.

    """
    def filter(self, record):
        if hasattr(record.request.user, 'email'):
            record.request.META['CURRENT_USER'] = record.request.user.email
        return True


class FilterIgnorable404URLs(logging.Filter):
    """
    Takes the IGNORABLE_404_URLS setting and disables logging for mathing URLs.

    Add it to your logging filters like so::

        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'filter_ignorable_404_urls': {
                '()': 'django_libs.utils_log.FilterIgnorable404URLs'
            }
        },

    Apply the filter to your handlers like so::

        'handlers': {
            'mail_admins': {
                'level': 'WARNING',
                'filters': ['require_debug_false', filter_ignorable_404_urls', ],  # NOQA
                'class': 'django.utils.log.AdminEmailHandler'
            },

    """
    def filter(self, record):
        request = record.request

        if record.status_code != 404:
            # No 404? No business for this filter.
            return True

        path = request.get_full_path()
        is_ignorable = any(
            pattern.search(path) for pattern in settings.IGNORABLE_404_URLS)
        if is_ignorable:
            return False

        return True
