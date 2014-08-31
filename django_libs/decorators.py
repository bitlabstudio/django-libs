"""Kept for backwards compatibility. Please add everything to the path below."""
import warnings

from .utils.decorators import *  # NOQA

warnings.warn('Please import from django_libs.utils.decorators instead.',
              DeprecationWarning)
