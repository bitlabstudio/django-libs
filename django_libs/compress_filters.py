"""Kept for backwards compatibility. Please add everything to the path below."""
import warnings

from .utils.compress_filters import *  # NOQA

warnings.warn('Please import from django_libs.utils.compress_filters instead.',
              DeprecationWarning)
