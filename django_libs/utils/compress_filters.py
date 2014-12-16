"""Custom filters for the ``compressor`` app."""
from django.conf import settings

from compressor.filters.css_default import CssAbsoluteFilter
from compressor.utils import staticfiles


class S3CssAbsoluteFilter(CssAbsoluteFilter):
    """
    This CSS filter was built to use django-compressor in combination with a
    Amazon S3 storage. It will make sure to provide the right URLs, whether
    you're in DEBUG mode or not.

    Make sure to add the ``FULL_DOMAIN`` setting. This is your base url, e.g.
    'https://www.example.com'.

    """
    def __init__(self, *args, **kwargs):
        super(S3CssAbsoluteFilter, self).__init__(*args, **kwargs)
        self.url = '%s%s' % (settings.FULL_DOMAIN, settings.STATIC_URL)
        self.url_path = self.url

    def find(self, basename):
        # The line below is the original line.  I removed settings.DEBUG.
        # if settings.DEBUG and basename and staticfiles.finders:
        if basename and staticfiles.finders:
            return staticfiles.finders.find(basename)
