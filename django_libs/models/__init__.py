"""Kept for backwards compatibility. Please add everything to the path below."""
from .fields import *  # NOQA

raise DeprecationWarning(
    'Please import from django_libs.models.fields instead.')
