"""Tests for the utility functions in ``loaders.py``."""
from django.test import TestCase

from ..loaders import load_member, load_member_from_setting, split_fqn


def callable_that_returns_fqn_string():
    """Dummy function Used by tests."""
    return 'django_libs.loaders.load_member'


class LoadMemberTestCase(TestCase):
    """Tests for the ``load_member`` utility function."""
    def test_function(self):
        member = load_member('django_libs.loaders.load_member')
        self.assertEqual(member.__name__, 'load_member')


class LoadMemberFromSetting(TestCase):
    """Tests for the ``load_member_from_setting`` utility function."""
    def test_function(self):
        member = load_member_from_setting('TEST_LOAD_MEMBER')
        self.assertEqual(member.__name__, 'load_member')


class SplitFqnTestCase(TestCase):
    """Tests for the ``split_fqn`` utility function."""
    def test_with_string(self):
        modulename, membername = split_fqn('django_libs.loaders.load_member')
        self.assertEqual(modulename, 'django_libs.loaders')
        self.assertEqual(membername, 'load_member')

    def test_with_callable(self):
        modulename, membername = split_fqn(callable_that_returns_fqn_string)
        self.assertEqual(modulename, 'django_libs.loaders')
        self.assertEqual(membername, 'load_member')
