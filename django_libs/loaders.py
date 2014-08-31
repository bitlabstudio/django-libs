"""Kept for backwards compatibility. Please add everything to the path below."""
import warnings

from .utils.loaders import *  # NOQA

warnings.warn('Please import from django_libs.utils.loaders instead.',
              DeprecationWarning)
