"""Useful mixins for models."""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import get_language

from hvad.models import NoTranslation, TranslationManager


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
        return self.get_queryset().filter(**kwargs)


@python_2_unicode_compatible
class TranslationModelMixin(object):
    """Mixin to provide custom django-hvad overrides."""
    def __str__(self):
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
