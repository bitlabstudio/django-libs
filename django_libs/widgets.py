"""Kept for backwards compatibility. Please add everything to the path below."""
import warnings

from .forms.widgets import *  # NOQA

warnings.warn(
    'Please import from django_libs.forms.widgets instead.', DeprecationWarning)
