"""Tests for the log utils of ``django_libs``."""
from django.test import TestCase

from mock import Mock

from ...utils.log import AddCurrentUser, FilterIgnorable404URLs


class AddCurrentUserTestCase(TestCase):
    """Tests for the ``AddCurrentUser`` filter."""
    longMessage = True

    def test_filter(self):
        user = Mock()
        user.email = 'foo@example.com'
        record = Mock()
        record.request.user = user
        record.request.META = {}
        self.assertTrue(AddCurrentUser().filter(record))


class FilterIgnorable404URLsTestCase(TestCase):
    """Tests for the ``FilterIgnorable404URLs`` filter."""
    longMessage = True

    def test_filter(self):
        record = Mock()
        record.status_code = 200
        record.request.META = {
            'HTTP_USER_AGENT': 'Mozilla/5.0 (compatible; bingbot/2.0;'
                               ' +http://www.bing.com/bingbot.htm)',
        }
        self.assertTrue(FilterIgnorable404URLs().filter(record))
        record.status_code = 404
        self.assertFalse(FilterIgnorable404URLs().filter(record))
        record.request.META.update({
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows Phone 8.1; ARM;'
                               ' Trident/7.0; Touch; rv:11.0; IEMobile/11.0;'
                               ' NOKIA; Lumia 530) like Gecko'})
        record.request.get_full_path = Mock(return_value='/foo/')
        self.assertTrue(FilterIgnorable404URLs().filter(record))
        record.request.get_full_path = Mock(return_value='/static/logo.png')
        self.assertFalse(FilterIgnorable404URLs().filter(record))
