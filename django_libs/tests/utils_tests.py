"""Tests for the utils of ``django_libs``."""
import os

from django.test import TestCase

from ..utils import (
    conditional_decorator, create_random_string, html_to_plain_text)
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
        path = os.path.dirname(os.path.abspath(__file__)) + (
            '/test_app/templates/html_email.html')
        with open(path, 'rb') as file:
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
