"""Tests for the utils of ``django_libs``."""
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import SiteProfileNotAvailable

from ..utils import get_profile
from .factories import UserFactory
from test_app.models import DummyProfile


def get_profile_method(user):
    return DummyProfile.objects.get_or_create(user=user)[0]


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
