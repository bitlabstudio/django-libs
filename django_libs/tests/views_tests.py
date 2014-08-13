"""Tests for the view classes of ``django-libs``."""
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.views.generic import TemplateView, View

from .. import views
from .factories import UserFactory
from .mixins import ViewTestMixin, ViewRequestFactoryTestMixin


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
        self.assertRaises(TypeError, views.HybridView.as_view, **bad_kwargs)

        bad_kwargs = self.view_kwargs.copy()
        bad_kwargs.update({'wrongattr': 'this is not defined on the view'})
        self.assertRaises(TypeError, views.HybridView.as_view, **bad_kwargs)

        self.should_be_callable_when_authenticated(self.user)


class PaginatedCommentAJAXViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``PaginatedCommentAJAXView`` view class."""
    view_class = views.PaginatedCommentAJAXView

    def setUp(self):
        self.user = UserFactory()
        self.comment = Comment.objects.create(
            content_type=ContentType.objects.get(name='user'),
            object_pk=self.user.pk,
            comment='foobar',
            site=Site.objects.create(),
        )

    def test_view(self):
        self.is_not_callable()
        self.is_callable(ajax=True)


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
        self.assertEqual(resp.content, 'done')


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
        self.assertEqual(resp.content, 'done')
