"""Tests for the models of the ``django_libs`` app."""
from django.test import TestCase

from ..models import ColorField
from ..widgets import ColorPickerWidget


class ColorFieldTestCase(TestCase):
    """Tests for the ``ColorField`` model."""
    longMessage = True

    def test_functions(self):
        color_field = ColorField()
        color_field.formfield
        self.assertIsInstance(
            color_field.formfield().widget, ColorPickerWidget, msg=(
                'Should add the color field widget.'))
