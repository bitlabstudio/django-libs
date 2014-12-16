"""Kept for backwards compatibility. Please add everything to the path below."""
import warnings

from .models.mixins import *  # NOQA

warnings.warn('Please import from django_libs.models.mixins instead.',
              DeprecationWarning)
