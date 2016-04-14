"""Kept for backwards compatibility."""
import warnings

from .utils.email import *  # NOQA


warnings.warn('Please import from django_libs.utils.email instead.',
              DeprecationWarning)
