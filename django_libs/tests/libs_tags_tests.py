"""Tests for the templatetags of the ``project-kairos`` project."""
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from django_libs.templatetags.libs_tags import *  # NOQA


class GetRangeTestCase(TestCase):
    """Tests for the ``get_range`` filter."""
    longMessage = True

    def test_filter(self):
        result = get_range(5)
        self.assertEqual(result, range(5), msg=(
            "Filter should behave exactly like Python's range function"))


class LoadContextNodeTestCase(TestCase):
    """Tests for the ``LoadContextNode`` template node."""
    def test_node(self):
        node = LoadContextNode('django_libs.tests.test_context')
        context = {}
        node.render(context)
        self.assertEqual(context['FOO'], 'bar')
        self.assertEqual(context['BAR'], 'foo')


class NavactiveTestCase(TestCase):
    """Tests for the ``navactive`` templatetag."""
    longMessage = True

    def test_tag(self):
        req = RequestFactory().get('/home/')
        result = navactive(req, '/home/')
        self.assertEqual(result, 'active', msg=(
            "When the given string is part of the current request's URL path"
            " it should return ``active`` but returned %s" % result))
        result = navactive(req, '/foo/')
        self.assertEqual(result, '', msg=(
            "When the given string is not part of the current request's URL"
            " path it should return '' but returned %s" % result))

        req = RequestFactory().get('/')
        result = navactive(req, '/', exact=True)
        self.assertEqual(result, 'active', msg=(
            "When the given string is equal to the current request's URL path"
            " it should return ``active`` but returned %s" % result))
        result = navactive(req, '/foo/', exact=True)
        self.assertEqual(result, '', msg=(
            "When the given string is not equal to the current request's URL"
            " path it should return '' but returned %s" % result))

        req = RequestFactory().get('/index/test/')
        result = navactive(req, 'index')
        self.assertEqual(result, 'active', msg=(
            "When the given string is a url name, it should return"
            " 'active', if it matches the path, but returned %s" % result))

        req = RequestFactory().get('/index/test/')
        result = navactive(req, '/index/test/')
        self.assertEqual(result, 'active', msg=(
            "When the given string is a long string, it should return"
            " 'active', if it matches the path, but returned %s" % result))

        result = navactive(req, 'home')
        self.assertEqual(result, '', msg=(
            "When the given string is a url name, it should return"
            " '', if it matches the path, but returned %s" % result))


class RenderAnalyticsCodeTestCase(TestCase):
    """Tests for the ``render_analytics_code`` templatetag."""
    longMessage = True

    def test_tag(self):
        result = render_analytics_code()
        expected = {
            'ANALYTICS_TRACKING_ID': 'UA-XXXXXXX-XX',
            'anonymize_ip': 'anonymize'
        }
        self.assertEqual(result, expected, msg=('Should return a dict.'))


class VerbatimTestCase(TestCase):
    """Tests for the ``verbatim`` template tag."""
    longMessage = True

    def test_tag(self):
        template = Template(
            '{% load libs_tags %}{% verbatim %}{% if test1 %}{% test1 %}'
            '{% endif %}{{ test2 }}{% endverbatim %}')
        self.assertEqual(template.render(Context()),
                         '{% if test1 %}{% test1 %}{% endif %}{{ test2 }}')
