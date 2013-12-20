"""Tests for the forms utilities of django_libs."""
from django import forms
from django.test import TestCase

from .. import forms as libs_forms


class DummyForm(libs_forms.StripTagsFormMixin, forms.Form):
    text = forms.CharField(max_length=1024)

    STRIP_TAGS_FIELDS = ['text', ]

    def __init__(self, *args, **kwargs):
        super(DummyForm, self).__init__(*args, **kwargs)
        self.strip_tags()


class StripTagsFormMixinTestCase(TestCase):
    """Tests for the ``StripTagsFormMixin``."""
    longMessage = True

    def test_mixin(self):
        form = DummyForm(data={'text': '<em>Foo</em>'})
        self.assertEqual(form.data['text'], 'Foo', msg=(
            'The mixin should strip away the tags from the given form data'))

        form = DummyForm(prefix='bar', data={'bar-text': '<em>Foo</em>'})
        self.assertEqual(form.data['bar-text'], 'Foo', msg=(
            'The mixin still works when the form has a prefix'))
