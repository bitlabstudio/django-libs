"""Tests for the text utils of ``django_libs``."""
from django.test import TestCase

from ...utils.text import create_random_string


class CreateRandomStringTestCase(TestCase):
    """Tests for the ``create_random_string`` function."""
    longMessage = True

    def test_func(self):
        self.assertEqual(len(create_random_string()), 7, msg=(
            'Should return a random string with 7 characters.'))
        self.assertEqual(
            len(create_random_string(length=3, chars='ABC', repetitions=True)),
            3, msg=('Should return a random string with 3 characters.'))
