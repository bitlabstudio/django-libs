"""Tests for the utils of ``django_libs``."""
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import SiteProfileNotAvailable

from ..utils import (
    conditional_decorator,
    create_random_string,
    get_profile,
    html_to_plain_text,
)
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


class CreateRandomStringTestCase(TestCase):
    """Tests for the ``create_random_string`` function."""
    longMessage = True

    def test_func(self):
        self.assertEqual(len(create_random_string()), 7, msg=(
            'Should return a random string with 7 characters.'))
        self.assertEqual(
            len(create_random_string(length=3, chars='ABC', repetitions=True)),
            3, msg=('Should return a random string with 3 characters.'))


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


class HTMLToPlainTextTestCase(TestCase):
    """Tests for the ``html_to_plain_text`` function."""
    longMessage = True

    def test_html_to_plain_text(self):
        html = (
            """
            <html>
                    <head></head>
                    <body>
                        <ul>
                            <li>List element</li>
                            <li>List element</li>
                            <li>List element</li>
                        </ul>
                    </body>
                </html>
            """
        )
        self.assertEqual(
            html_to_plain_text(html),
            '\n  * List element\n  * List element\n  * List element',
            msg='Should return a formatted plain text.')
        with open('test_app/templates/html_email.html', 'rb') as file:
            self.assertIn('[1]: *|ARCHIVE|*\n', html_to_plain_text(file), msg=(
                'Should return a formatted plain text.'))

    def test_replace_links(self):
        html = (
            """
            <span>T1<span> <a href="www.example.com">link</a> <span>T2</span>
            <br />
            <span>T3</span>
            """
        )
        expected = (
            "T1 link[1] T2\nT3\n\n[1]: www.example.com\n"
        )
        result = html_to_plain_text(html)
        self.assertEqual(result, expected, msg=(
            'Should replace links nicely'))

    def test_replace_br(self):
        html = (
            """
            <span>Text1</span>
            <br />
            <br />
            <span>Text2</span>
            """
        )
        expected = (
            "Text1\n\nText2"
        )
        result = html_to_plain_text(html)
        self.assertEqual(result, expected, msg=(
            'Should replace links nicely'))
