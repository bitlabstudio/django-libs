"""Tests for the model mixins of ``django_libs``."""
from django.test import TestCase
from django.utils.translation import activate

from .test_app.factories import ParlerDummyFactory
from .test_app.models import ParlerDummy


class TranslationModelMixinTestCase(TestCase):
    """Tests for the ``TranslationModelMixin`` model mixin."""
    longMessage = True

    def test_functions(self):
        translated_obj = ParlerDummyFactory()
        self.assertEqual(translated_obj.translation_getter('title'), 'title0')
        untranslated_obj = ParlerDummy()
        self.assertIsNone(untranslated_obj.translation_getter('title'))
        untranslated_obj.set_current_language('de')
        untranslated_obj.title = 'DE'
        untranslated_obj.save()
        activate('de')
        self.assertEqual(untranslated_obj.translation_getter('title'), 'DE')
        activate('en')
