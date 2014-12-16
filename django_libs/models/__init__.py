"""Kept for backwards compatibility. Please add everything to the path below."""
import warnings
from .fields import *  # NOQA

warnings.warn('Please import from django_libs.models.fields instead.',
              DeprecationWarning)
