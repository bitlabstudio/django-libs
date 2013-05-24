"""Useful mixins for models."""
from django.db import models
from django.utils.translation import get_language

from simple_translation.utils import get_preferred_translation_from_lang


class SimpleTranslationMixin(object):
    """Adds a ``get_translation`` method to the model."""
    def get_translation(self, language=None):
        """
        Returns the translation object for this object.

        :param language: A string representing a language (i.e. 'en'). If not
          given we will use the currently active language.

        """
        lang = language or get_language()
        return get_preferred_translation_from_lang(self, lang)


class SimpleTranslationPublishedManager(models.Manager):
    """
    Can be inherited by a custom manager, to add filtering for published
    objects, optionally with language specific filtering.

    The custom Manager needs to set ``published_field`` and ``language_field``
    to point to the fields, that hold the published state and the language.

    If those fields are not set on the child manager, it is assumed, that the
    model holding the translation fields for "Object" is called
    "ObjectTranslation". That way you can use this directly as a manager, if
    you stick to that pattern.

    """
    def published(self, request, check_language=True):
        """
        Returns all objects, which are published and in the currently
        active language if check_language is True (default).

        :param request: A Request instance.
        :param check_language: Option to disable language filtering.

        """
        published_field = getattr(
            self, 'published_field',
            '{}translation__is_published'.format(
                self.model._meta.module_name))
        filter_kwargs = {published_field: True, }
        results = self.get_query_set().filter(**filter_kwargs)

        if check_language:
            language = getattr(request, 'LANGUAGE_CODE', None)
            if not language:
                self.model.objects.none()
            language_field = getattr(
                self, 'language_field',
                '{}translation__language'.format(
                    self.model._meta.module_name))
            language_filter_kwargs = {language_field: language}
            results = results.filter(**language_filter_kwargs)

        return results.distinct()
