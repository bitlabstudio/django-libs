"""Additions for the django admin."""
from django.utils.translation import ugettext_lazy as _


class MultilingualPublishMixin(object):
    """Mixin to provide common methods for multilingual object admins."""

    def is_published(self, obj):
        languages = ''
        for trans in obj.translations:
            if trans.is_published:
                if languages == '':
                    languages = trans.language
                else:
                    languages += ', {0}'.format(trans.language)
        if languages == '':
            return _('Not published')
        return languages
    is_published.short_description = _('Is published')
