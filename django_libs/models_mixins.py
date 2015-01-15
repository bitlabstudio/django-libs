"""Useful mixins for models."""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import get_language

from hvad.models import NoTranslation, TranslationManager
from simple_translation.utils import get_preferred_translation_from_lang


class HvadPublishedManager(TranslationManager):
    """
    Returns all objects, which are published and in the currently
    active language if check_language is True (default).

    :param request: A Request instance.
    :param check_language: Option to disable language filtering.

    """
    def published(self, request, check_language=True):
        kwargs = {'translations__is_published': True}
        if check_language:
            language = getattr(request, 'LANGUAGE_CODE', get_language())
            if not language:
                self.model.objects.none()
            kwargs.update({'translations__language_code': language})
        return self.get_query_set().filter(**kwargs)


class TranslationModelMixin(object):
    """Mixin to provide custom django-hvad overrides."""
    def __unicode__(self):
        return self.translation_getter('title')

    def check_for_result(self, language, translation, result, name):
        if not result:
            try:
                translation = self.translations.get(language_code=language)
            except ObjectDoesNotExist:
                pass
            else:  # pragma: nocover
                result = getattr(translation, name, '')
        return translation, result

    def translation_getter(self, name):
        """
        Custom translation getter.

        1. Try the current language
        2. Try base language (e.g. 'en' instead of 'en-gb')
        3. Try default sys language
        4. Use any translation

        """
        stuff = self.safe_translation_getter(name, NoTranslation)
        if stuff is not NoTranslation:
            return stuff

        translation = None
        result = None

        # Check for the current language
        translation, result = self.check_for_result(
            get_language(), translation, result, name)

        # Check for the current main language
        translation, result = self.check_for_result(
            get_language()[:2], translation, result, name)

        # Check for the default language
        translation, result = self.check_for_result(
            settings.LANGUAGE_CODE, translation, result, name)

        if not result:
            # Check for any available language
            for trans in self.translations.all():  # pragma: nocover
                translation = trans
                result = getattr(translation, name, '')
                if result:
                    break

        setattr(self, self._meta.translations_cache, translation)
        return result


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
