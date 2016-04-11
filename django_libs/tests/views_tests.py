"""Tests for the view classes of ``django-libs``."""
from django.test import TestCase

from .. import views
from .mixins import ViewRequestFactoryTestMixin


class RapidPrototypingViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``RapidPrototypingView`` view class."""
    longMessage = True

    def setUp(self):
        self.view_class = views.RapidPrototypingView

    def get_view_name(self):
        return 'prototype'

    def get_view_kwargs(self):
        return {'template_path': 'django_libs/analytics.html'}

    def test_view(self):
        self.is_callable()


class UpdateSessionAJAXViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``UpdateSessionAJAXView`` view class."""
    longMessage = True

    def setUp(self):
        self.view_class = views.UpdateSessionAJAXView

    def get_view_name(self):
        return 'update_session'

    def test_view(self):
        self.is_forbidden()
        data = {'session_name': 'foo', 'session_value': 'bar'}
        resp = self.is_postable(ajax=True, data=data)
        self.assertEqual(resp.content, b'done')


class UpdateCookieAJAXViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``UpdateCookieAJAXView`` view class."""
    longMessage = True

    def setUp(self):
        self.view_class = views.UpdateCookieAJAXView

    def get_view_name(self):
        return 'update_cookie'

    def test_view(self):
        self.is_forbidden()
        data = {'cookie_key': 'foo', 'cookie_value': 'bar'}
        resp = self.is_postable(ajax=True, data=data)
        self.assertEqual(resp.content, b'done')
