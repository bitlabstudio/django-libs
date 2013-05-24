"""Tests for the model mixins of ``django_libs``."""
from mock import Mock

from django.test import TestCase

from .test_app.factories import DummyProfileTranslationFactory
from .test_app.models import DummyProfile


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
