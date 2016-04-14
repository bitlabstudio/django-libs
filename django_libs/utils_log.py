"""Kept for backwards compatibility."""
import warnings

from .utils.log import *  # NOQA


warnings.warn('Please import from django_libs.utils.log instead.',
              DeprecationWarning)
