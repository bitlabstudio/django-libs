"""Tests for the templatetags of the ``project-kairos`` project."""
from mock import Mock, patch

from django.template import Context, Template
from django.test import RequestFactory, TestCase

from django_libs.templatetags.libs_tags import *  # NOQA
from .test_app.factories import DummyProfileFactory


class CalculateDimensionsTestCase(TestCase):
    """Tests for the ``calculate_dimensions`` templatetag."""
    longMessage = True

    def test_tag(self):
        image = Mock()
        image.width = 1
        image.height = 2
        result = calculate_dimensions(image, 20, 10)
        self.assertEqual(result, '10x20', msg=(
            'If the width is smaller than the height, the thumbnail should'
            ' also have a smaller width'))

        image.width = 2
        image.height = 1
        result = calculate_dimensions(image, 20, 10)
        self.assertEqual(result, '20x10', msg=(
            'If the width is bigger than the height, the thumbnail should'
            ' also have a bigger width'))

        image.width = 1
        image.height = 1
        result = calculate_dimensions(image, 20, 10)
        self.assertEqual(result, '20x10', msg=(
            'If the width is equal to the height, the thumbnail should'
            ' be in landscape format.'))


class CallTestCase(TestCase):
    """Tests for the ``call`` templatetag."""
    longMessage = True

    def setUp(self):
        self.func = lambda args: args
        self.obj = Mock(func=self.func)

    def test_tag(self):
        self.assertEqual(call(self.obj, 'func', 'test_string'), 'test_string')


class GetVerboseTestCase(TestCase):
    """Tests for the ``get_verbose`` templatetag."""
    longMessage = True

    def setUp(self):
        self.profile = DummyProfileFactory()

    def test_tag(self):
        self.assertEqual(
            get_verbose(self.profile, 'dummy_field'), 'Dummy Field',
            msg='Returned the wrong verbose name for the "dummy_field".')
        self.assertEqual(
            get_verbose(self.profile, 'non_existant_field'), '', msg=(
                'Should return "" for a non-existant field.'))


class GetProfileForTestCase(TestCase):
    """Tests for the ``get_profile_for`` templatetag."""
    longMessage = True

    def setUp(self):
        self.profile = DummyProfileFactory()
        self.user = self.profile.user

    def test_tag(self):
        self.assertEqual(get_profile_for(self.user), self.profile)


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

    @patch('django_libs.templatetags.libs_tags.resolve')
    def test_use_resolver_true(self, mock_resolve):
        req = RequestFactory().get('/index/test/')
        navactive(req, '/index/test/')
        self.assertTrue(mock_resolve.called, msg=(
            'When calling the tag normally, we will try to resolve the given'
            ' url.'))

    @patch('django_libs.templatetags.libs_tags.resolve')
    def test_use_resolver_false(self, mock_resolve):
        req = RequestFactory().get('/index/test/')
        navactive(req, '/index/test/', use_resolver=False)
        self.assertFalse(mock_resolve.called, msg=(
            'When calling the tag with use_resolve=False the resolver should'
            ' not be called at all'))


class GetRangeTestCase(TestCase):
    """Tests for the ``get_range`` filter."""
    longMessage = True

    def test_filter(self):
        result = get_range(5)
        self.assertEqual(result, range(5), msg=(
            "Filter should behave exactly like Python's range function"))

    def test_filter_with_max_num(self):
        result = get_range(3, 5)
        self.assertEqual(result, range(2), msg=(
            'Filter should return the difference between value and max_num'))


class RenderAnalyticsCodeTestCase(TestCase):
    """Tests for the ``render_analytics_code`` templatetag."""
    longMessage = True

    def test_tag(self):
        result = render_analytics_code()
        expected = {
            'ANALYTICS_TRACKING_ID': 'UA-THISISNOREAL-ID',
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
