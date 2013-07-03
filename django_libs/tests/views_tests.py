"""Tests for the view classes of ``django-libs``."""
from django.test import TestCase
from django.views.generic import TemplateView, View

from ..views import HybridView
from .factories import UserFactory
from .mixins import ViewTestMixin


class HybridViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``HybridView`` view class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()

        self.authed_view = TemplateView.as_view(template_name='base.html')
        self.authed_view_kwargs = {'authed': True}
        self.anonymous_view = TemplateView.as_view(template_name='base.html')
        self.anonymous_view_kwargs = {'anonymous': True}
        self.other_anonymous_view = View.as_view()
        self.view_kwargs = {
            'authed_view': self.authed_view,
            'authed_view_kwargs': self.authed_view_kwargs,
            'anonymous_view': self.anonymous_view,
            'anonymous_view_kwargs': self.anonymous_view_kwargs}

    def get_view_name(self):
        return self.view_name

    def test_view(self):
        self.view_name = 'dummy_hybrid'
        self.should_be_callable_when_anonymous()

        bad_kwargs = self.view_kwargs.copy()
        bad_kwargs.update({'post': 'this should not be defined here'})
        self.assertRaises(TypeError, HybridView.as_view, **bad_kwargs)

        bad_kwargs = self.view_kwargs.copy()
        bad_kwargs.update({'wrongattr': 'this is not defined on the view'})
        self.assertRaises(TypeError, HybridView.as_view, **bad_kwargs)

        self.should_be_callable_when_authenticated(self.user)


# class RapidPrototypingViewTestCase(ViewTestMixin, TestCase):
#     """Tests for the ``RapidPrototypingView`` view class."""
#     longMessage = True

#     def get_view_name(self):
#         return 'prototype'

#     def test_view(self):
#         self.should_be_callable_when_anonymous()
