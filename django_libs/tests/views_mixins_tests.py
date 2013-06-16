"""Tests for the view mixins of ``django-libs``."""
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic import TemplateView

from django_libs.views_mixins import AjaxResponseMixin


class DummyView(AjaxResponseMixin, TemplateView):
    """Just a test view."""
    template_name = "test_template.html"


class AjaxResponseMixinTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.view = DummyView()

    def test_mixin(self):
        """Test for the ``AjaxResponseMixin`` class."""
        extra = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        req = RequestFactory().get('/', **extra)
        self.view.request = req
        self.assertEqual(self.view.get_template_names(),
                         ['ajax_test_template.html'],
                         msg='Got the wrong template name.')
