"""Tests for the templatetags of the ``project-kairos`` project."""
from django.test import RequestFactory, TestCase

from django_libs.templatetags.libs_tags import *


class NavactiveTestCase(TestCase):
    """Tests for the ``navactive`` templatetag."""
    def test_tag(self):
        req = RequestFactory().get('/home/')
        result = navactive(req, 'home')
        self.assertEqual(result, 'active', msg=(
            "When the given string is part of the current request's URL path"
            " it should return ``active`` but returned %s" % result))
        result = navactive(req, 'foo')
        self.assertEqual(result, '', msg=(
            "When the given string is not part of the current request's URL"
            " path it should return '' but returned %s" % result))

        req = RequestFactory().get('/')
        result = navactive(req, '/', exact=True)
        self.assertEqual(result, 'active', msg=(
            "When the given string is equal to the current request's URL path"
            " it should return ``active`` but returned %s" % result))
        result = navactive(req, '/foo', exact=True)
        self.assertEqual(result, '', msg=(
            "When the given string is not equal to the current request's URL"
            " path it should return '' but returned %s" % result))
