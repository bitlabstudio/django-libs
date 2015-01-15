"""Tests for the model mixins of ``django_libs``."""
from mock import Mock

from django.test import TestCase
from django.utils.translation import activate

from .test_app.factories import (
    DummyProfileTranslationFactory,
    HvadDummyFactory,
)
from .test_app.models import DummyProfile, HvadDummy


class TranslationModelMixinTestCase(TestCase):
    """Tests for the ``TranslationModelMixin`` model mixin."""
    longMessage = True

    def test_functions(self):
        translated_obj = HvadDummyFactory()
        self.assertEqual(translated_obj.translation_getter('title'), 'title1')
        untranslated_obj = HvadDummy()
        self.assertIsNone(untranslated_obj.translation_getter('title'))
        untranslated_obj.translate('de')
        untranslated_obj.title = 'foo'
        untranslated_obj.save()
        activate('de')
        self.assertEqual(untranslated_obj.translation_getter('title'), 'foo')
        activate('en')


class SimpleTranslationMixinTestCase(TestCase):
    """Tests for the ``SimpleTranslationMixin`` mixin."""
    longMessage = True

    def setUp(self):
        self.dummyprofile_trans = DummyProfileTranslationFactory()
        self.dummyprofile = self.dummyprofile_trans.dummyprofile

    def test_mixin(self):
        self.assertEqual(self.dummyprofile.get_translation(),
                         self.dummyprofile_trans)


class SimpleTranslationPublishedManagerTestCase(TestCase):
    """Tests for the ``SimpleTranslationPublishedManager`` manager."""
    longMessage = True

    def setUp(self):
        DummyProfileTranslationFactory()
        DummyProfileTranslationFactory(is_published=False)
        DummyProfileTranslationFactory(language='de')
        DummyProfileTranslationFactory(language='de', is_published=False)

    def test_manager(self):
        request = Mock(LANGUAGE_CODE='en')
        self.assertEqual(DummyProfile.objects.published(request).count(), 1,
                         msg='There should be one published english dummy.')

        request = Mock(LANGUAGE_CODE='de')
        self.assertEqual(DummyProfile.objects.published(request).count(), 1,
                         msg='There should be one published german dummy.')

        request = Mock(LANGUAGE_CODE=None)
        self.assertEqual(DummyProfile.objects.published(request).count(), 0,
                         msg=(
                             'There should be no published dummy, if no'
                             ' language is set.'))
