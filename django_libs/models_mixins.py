"""Useful mixins for models."""
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
