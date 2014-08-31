"""Kept for backwards compatibility. Please add everything to the path below."""
from .forms.widgets import *  # NOQA

raise DeprecationWarning(
    'Please import from django_libs.forms.widgets instead.')
