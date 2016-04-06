"""Tests for the model mixins of ``django_libs``."""
from django.test import TestCase
from django.utils.translation import activate

from .test_app.factories import HvadDummyFactory
from .test_app.models import HvadDummy


class TranslationModelMixinTestCase(TestCase):
    """Tests for the ``TranslationModelMixin`` model mixin."""
    longMessage = True

    def test_functions(self):
        translated_obj = HvadDummyFactory()
        self.assertEqual(translated_obj.translation_getter('title'), 'title0')
        untranslated_obj = HvadDummy()
        self.assertIsNone(untranslated_obj.translation_getter('title'))
        untranslated_obj.translate('de')
        untranslated_obj.title = 'foo'
        untranslated_obj.save()
        activate('de')
        self.assertEqual(untranslated_obj.translation_getter('title'), 'foo')
        activate('en')
