"""Tests for the utils of ``django_libs``."""
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import SiteProfileNotAvailable

from ..utils import conditional_decorator, get_profile
from .factories import UserFactory
from test_app.models import DummyProfile


def dummy_decorator(func):
    def wrapper():
        return 0
    return wrapper


@conditional_decorator(dummy_decorator, False)
def test_method():
    """Used to test the ``conditional_decorator``."""
    return 1


@conditional_decorator(dummy_decorator, True)
def test_method_true():
    """Used to test the ``conditional_decorator``."""
    return 1


def get_profile_method(user):
    return DummyProfile.objects.get_or_create(user=user)[0]


class ConditionalDecoratorTestCase(TestCase):
    """Tests for the ``conditional_decorator``."""
    longMessage = True

    def test_decorator_with_condition_false(self):
        result = test_method()
        self.assertEqual(result, 1, msg=(
            'The method should have been executed normally, without calling'
            ' the decorator'))

    def test_decorator_with_condition_true(self):
        result = test_method_true()
        self.assertEqual(result, 0, msg=(
            'The method should have been executed with the decorator'))


class GetProfileTestCase(TestCase):
    """Tests for the ``get_profile`` function."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.old_get_profile_method = getattr(
            settings, 'GET_PROFILE_METHOD', None)
        self.old_auth_profile_module = getattr(
            settings, 'AUTH_PROFILE_MODULE', None)
        settings.AUTH_PROFILE_MODULE = (
            'test_app.DummyProfile')

    def tearDown(self):
        if self.old_get_profile_method:
            settings.GET_PROFILE_METHOD = self.old_get_profile_method
        if self.old_auth_profile_module:
            settings.AUTH_PROFILE_MODULE = self.old_auth_profile_module

    def test_returns_profile(self):
        """Test if the ``get_profile`` method returns a profile."""
        profile = get_profile(self.user)
        self.assertEqual(type(profile), DummyProfile, msg=(
            'The method should return a DummyProfile instance.'))

        settings.AUTH_PROFILE_MODULE = 'user_profileUserProfile'
        self.assertRaises(SiteProfileNotAvailable, get_profile, self.user)

        settings.AUTH_PROFILE_MODULE = 'test_app.DummyProfile'

        settings.GET_PROFILE_METHOD = (
            'django_libs.tests.utils_tests.get_profile_method')
        DummyProfile.objects.all().delete()

        profile = get_profile(self.user)
        self.assertEqual(type(profile), DummyProfile, msg=(
            'The method should return a DummyProfile instance.'))
