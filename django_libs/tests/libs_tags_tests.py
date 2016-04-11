"""Tests for the templatetags of the ``project-kairos`` project."""
from mock import Mock, patch

from django.contrib.contenttypes.models import ContentType
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from .factories import SiteFactory
from ..templatetags import libs_tags as tags
from .test_app.factories import DummyProfileFactory
from .test_app.models import DummyProfile


class CalculateDimensionsTestCase(TestCase):
    """Tests for the ``calculate_dimensions`` templatetag."""
    longMessage = True

    def test_tag(self):
        image = Mock()
        image.width = 1
        image.height = 2
        result = tags.calculate_dimensions(image, 20, 10)
        self.assertEqual(result, '10x20', msg=(
            'If the width is smaller than the height, the thumbnail should'
            ' also have a smaller width'))

        image.width = 2
        image.height = 1
        result = tags.calculate_dimensions(image, 20, 10)
        self.assertEqual(result, '20x10', msg=(
            'If the width is bigger than the height, the thumbnail should'
            ' also have a bigger width'))

        image.width = 1
        image.height = 1
        result = tags.calculate_dimensions(image, 20, 10)
        self.assertEqual(result, '20x10', msg=(
            'If the width is equal to the height, the thumbnail should'
            ' be in landscape format.'))


class CallTestCase(TestCase):
    """Tests for the ``call`` templatetag."""
    longMessage = True

    def setUp(self):
        self.func = lambda args: args
        self.obj = Mock(func=self.func)
        self.obj.member = 'foobar'
        self.obj.dictionary = {'foo': 'bar', }

    def test_tag(self):
        self.assertEqual(
            tags.call(self.obj, 'func', 'test_string'), 'test_string', msg=(
                "When using it against an object's function, that function"
                " should be called and it's return value should be returned"))

        self.assertEqual(
            tags.call(self.obj, 'member'), 'foobar', msg=(
                "When using it against an object's member, that member"
                " should be returned"))

        self.assertEqual(
            tags.call(self.obj, 'dictionary', 'foo'), 'bar', msg=(
                "When using it against an object's member and that member"
                " is a dict it should return the value of the given key"))


class ConcatenateTestCase(TestCase):
    """Tests for the ``concatenate`` templatetag."""
    longMessage = True

    def test_tag(self):
        result = tags.concatenate('foo', 'bar')
        self.assertEqual(result, 'foobar', msg=(
            'If no divider is specified, the given strings should just be'
            ' concatenated'))
        result = tags.concatenate('foo', 'bar', 'foobar')
        self.assertEqual(result, 'foobarfoobar', msg=(
            'We can concatenate any number of strings'))
        result = tags.concatenate('foo', 'bar', divider='_')
        self.assertEqual(result, 'foo_bar', msg=(
            'If divider kwarg is given, the strings should be concatenated'
            ' with the given divider.'))


class GetContentTypeTestCase(TestCase):
    """Tests for the ``get_content_type`` templatetag."""
    longMessage = True

    def setUp(self):
        self.profile = DummyProfileFactory()

    def test_tag(self):
        self.assertIsInstance(
            tags.get_content_type(self.profile), ContentType,
            msg='Should return the profile\'s content type.')
        self.assertEqual(
            tags.get_content_type(self.profile, 'model'), 'dummyprofile',
            msg='Should return the profile\'s content type field model.')


class GetVerboseTestCase(TestCase):
    """Tests for the ``get_verbose`` templatetag."""
    longMessage = True

    def setUp(self):
        self.profile = DummyProfileFactory()

    def test_tag(self):
        self.assertEqual(
            tags.get_verbose(self.profile, 'dummy_field'), 'Dummy Field',
            msg='Returned the wrong verbose name for the "dummy_field".')
        self.assertEqual(
            tags.get_verbose(self.profile, 'non_existant_field'), '', msg=(
                'Should return "" for a non-existant field.'))


class GetQueryParamsTestCase(TestCase):
    """Tests for the ``get_query_params`` templatetag."""
    longMessage = True

    def test_tag(self):
        req = RequestFactory().get('/?foobar=1&barfoo=2')

        result = tags.get_query_params(req, 'foobar', 2)
        self.assertIn('foobar=2', result, msg=(
            'Should change the existing query parameter'))
        self.assertIn('barfoo=2', result, msg=(
            'Should change the existing query parameter'))

        result = tags.get_query_params(req, 'page', 2)
        self.assertIn('foobar=1', result, msg=(
            'Should change the existing query parameter'))
        self.assertIn('barfoo=2', result, msg=(
            'Should change the existing query parameter'))
        self.assertIn('page=2', result, msg=(
            'Should change the existing query parameter'))

        result = tags.get_query_params(req, 'page', 2, 'new', 42)
        self.assertIn('foobar=1', result, msg=(
            'Should change the existing query parameter'))
        self.assertIn('barfoo=2', result, msg=(
            'Should change the existing query parameter'))
        self.assertIn('page=2', result, msg=(
            'Should change the existing query parameter'))
        self.assertIn('new=42', result, msg=(
            'Should change the existing query parameter'))

        result = tags.get_query_params(req, 'page', 2, 'barfoo', '!remove')
        self.assertIn('foobar=1', result, msg=(
            'Should add new parameters and remove the ones marked for'
            ' removal'))
        self.assertIn('page=2', result, msg=(
            'Should add new parameters and remove the ones marked for'
            ' removal'))

        result = tags.get_query_params(req, 'page', 2, 'ghost', '!remove')
        self.assertIn('foobar=1', result, msg=(
            'Should not crash if the parameter marked for removal does not'
            ' exist'))
        self.assertIn('barfoo=2', result, msg=(
            'Should not crash if the parameter marked for removal does not'
            ' exist'))
        self.assertIn('page=2', result, msg=(
            'Should not crash if the parameter marked for removal does not'
            ' exist'))


class LoadContextNodeTestCase(TestCase):
    """Tests for the ``LoadContextNode`` template node."""
    def test_node(self):
        node = tags.LoadContextNode('django_libs.tests.test_context')
        context = {}
        node.render(context)
        self.assertEqual(context['FOO'], 'bar')
        self.assertEqual(context['BAR'], 'foo')


class NavactiveTestCase(TestCase):
    """Tests for the ``navactive`` templatetag."""
    longMessage = True

    def test_tag(self):
        req = RequestFactory().get('/home/')
        result = tags.navactive(req, '/home/')
        self.assertEqual(result, 'active', msg=(
            "When the given string is part of the current request's URL path"
            " it should return ``active`` but returned %s" % result))
        result = tags.navactive(req, '/foo/')
        self.assertEqual(result, '', msg=(
            "When the given string is not part of the current request's URL"
            " path it should return '' but returned %s" % result))

        req = RequestFactory().get('/')
        result = tags.navactive(req, '/', exact=True)
        self.assertEqual(result, 'active', msg=(
            "When the given string is equal to the current request's URL path"
            " it should return ``active`` but returned %s" % result))
        result = tags.navactive(req, '/foo/', exact=True)
        self.assertEqual(result, '', msg=(
            "When the given string is not equal to the current request's URL"
            " path it should return '' but returned %s" % result))

        req = RequestFactory().get('/index/test/')
        result = tags.navactive(req, 'index')
        self.assertEqual(result, 'active', msg=(
            "When the given string is a url name, it should return"
            " 'active', if it matches the path, but returned %s" % result))

        req = RequestFactory().get('/index/test/')
        result = tags.navactive(req, '/index/test/')
        self.assertEqual(result, 'active', msg=(
            "When the given string is a long string, it should return"
            " 'active', if it matches the path, but returned %s" % result))

        result = tags.navactive(req, 'home')
        self.assertEqual(result, '', msg=(
            "When the given string is a url name, it should return"
            " '', if it matches the path, but returned %s" % result))

    @patch('django_libs.templatetags.libs_tags.resolve')
    def test_use_resolver_true(self, mock_resolve):
        req = RequestFactory().get('/index/test/')
        tags.navactive(req, '/index/test/')
        self.assertTrue(mock_resolve.called, msg=(
            'When calling the tag normally, we will try to resolve the given'
            ' url.'))

    @patch('django_libs.templatetags.libs_tags.resolve')
    def test_use_resolver_false(self, mock_resolve):
        req = RequestFactory().get('/index/test/')
        tags.navactive(req, '/index/test/', use_resolver=False)
        self.assertFalse(mock_resolve.called, msg=(
            'When calling the tag with use_resolve=False the resolver should'
            ' not be called at all'))


class GetRangeTestCase(TestCase):
    """Tests for the ``get_range`` filter."""
    longMessage = True

    def test_filter(self):
        result = tags.get_range(5)
        self.assertEqual(result, range(5), msg=(
            "Filter should behave exactly like Python's range function"))

    def test_filter_with_max_num(self):
        result = tags.get_range(3, 5)
        self.assertEqual(result, range(2), msg=(
            'Filter should return the difference between value and max_num'))


class GetRangeAround(TestCase):
    """Tests for the ``get_range_around`` assignment tag."""
    longMessage = True

    def test_tag(self):
        result = tags.get_range_around(1, 1, 2)
        self.assertEqual(list(result['range_items']), [1], msg=(
            'If only one value given, return that value'))
        self.assertFalse(result['left_padding'])
        self.assertFalse(result['right_padding'])

        result = tags.get_range_around(5, 1, 2)
        self.assertEqual(list(result['range_items']), [1, 2, 3, 4, 5], msg=(
            'If padding is so small, that all values fit into the range,'
            ' return all values.'))
        self.assertFalse(result['left_padding'])
        self.assertFalse(result['right_padding'])

        result = tags.get_range_around(6, 1, 2)
        self.assertEqual(list(result['range_items']), [1, 2, 3, 4, 5], msg=(
            'If center value is at the beginning of the range, return desired'
            ' amount of values after the center value.'))
        self.assertFalse(result['left_padding'])
        self.assertTrue(result['right_padding'])

        result = tags.get_range_around(6, 6, 2)
        self.assertEqual(list(result['range_items']), [2, 3, 4, 5, 6], msg=(
            'If center value is at the end of the range, return desired'
            ' amount of values from the end of the range.'))
        self.assertTrue(result['left_padding'])
        self.assertFalse(result['right_padding'])

        result = tags.get_range_around(8, 2, 2)
        self.assertEqual(list(result['range_items']), [1, 2, 3, 4, 5], msg=(
            'If center value is so close to the left bound that the distance'
            ' from left bound to center value is less or equal to the'
            ' padding, return the range beginning from the left bound'))
        self.assertFalse(result['left_padding'])
        self.assertTrue(result['right_padding'])

        result = tags.get_range_around(8, 6, 2)
        self.assertEqual(list(result['range_items']), [4, 5, 6, 7, 8], msg=(
            'If center value is so close to the right bound that the distance'
            ' from right bound to center value is less or equal to the'
            ' padding, return the range so that it ends at the center value'))
        self.assertTrue(result['left_padding'])
        self.assertFalse(result['right_padding'])

        result = tags.get_range_around(10, 5, 2)
        self.assertEqual(list(result['range_items']), [3, 4, 5, 6, 7], msg=(
            'If center value is in the middle of the range, return center'
            ' value surrounded by padding values'))
        self.assertTrue(result['left_padding'])
        self.assertTrue(result['right_padding'])


class RenderAnalyticsCodeTestCase(TestCase):
    """Tests for the ``render_analytics_code`` templatetag."""
    longMessage = True

    def test_tag(self):
        result = tags.render_analytics_code()
        expected = {
            'ANALYTICS_TRACKING_ID': 'UA-THISISNOREAL-ID',
            'ANALYTICS_DOMAIN': 'auto',
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


class ExcludeTestCase(TestCase):
    """Tests for the ``exclude`` templatetag."""
    longMessage = True

    def setUp(self):
        self.dummy = DummyProfileFactory()
        DummyProfileFactory()
        DummyProfileFactory()
        DummyProfileFactory()

    def test_tag(self):
        qs = DummyProfile.objects.all()
        self.assertFalse(tags.exclude(qs, qs), msg=(
            'Should return an empty queryset, if both provided querysets are'
            ' identical.'))
        self.assertEqual(
            tags.exclude(qs, qs.exclude(pk=self.dummy.pk)).count(), 1,
            msg=('Should return one profile.'))


class IsContextVariableTestCase(TestCase):
    """Tests for the ``is_context_variable`` templatetag."""
    longMessage = True

    def test_tag(self):
        result = tags.is_context_variable({}, 'variable_name')
        self.assertEqual(result, False, msg=(
            'Should return False if the variable is not in the context'))

        context = {'variable_name': 1, }
        result = tags.is_context_variable(context, 'variable_name')
        self.assertEqual(result, True, msg=(
            'Should return True if the variable is in the context'))


class SumTestCase(TestCase):
    """Tests for the ``sum`` templatetag."""
    longMessage = True

    def test_tag(self):
        context = Mock()
        context.dicts = ({}, )
        key = 'foobar'
        tags.sum(context, key, 10)
        self.assertEqual(context.dicts[0][key], 10, msg=(
            'If the key does not exist, it will be added with the value 0, '
            ' then the given value will be added to that'))

        tags.sum(context, key, 15)
        self.assertEqual(context.dicts[0][key], 25, msg=(
            'If the key exist, the given value will be added to the existing, '
            ' value'))

        tags.sum(context, key, 15, -1)
        self.assertEqual(context.dicts[0][key], 10, msg=(
            'If a multiplier is given, the given value should be multiplied'
            ' before being added to the existing context value'))


class AppendSTestCase(TestCase):
    """Tests for the ``append_s`` template tag."""
    longMessage = True

    def test_tag(self):
        self.assertEqual(tags.append_s('Hans'), "Hans'", msg=(
            'If the input value ends with an "s", it should only append an'
            ' apostrohpe.'
        ))
        self.assertEqual(tags.append_s('Susi'), "Susi's", msg=(
            'If the input value does not end with an "s", it should append an'
            ' apostrohpe and an "s".'
        ))


class GetSiteTestCase(TestCase):
    """Tests for the ``get_site`` templatetag."""
    longMessage = True

    def setUp(self):
        self.site = SiteFactory()

    def test_tag(self):
        self.assertEqual(tags.get_site().domain, 'example.com')
