"""Logging related utilities."""
import logging
import re

from django.conf import settings
from django.utils.encoding import force_text


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

        referer = force_text(
            request.META.get('HTTP_REFERER', ''), errors='replace')
        if not referer:
            # Probably a user manipulating URL, do not log this
            return False

        path = request.get_full_path()
        is_ignorable = any(
            pattern.search(path) for pattern in settings.IGNORABLE_404_URLS)
        if is_ignorable:
            return False

        return True
