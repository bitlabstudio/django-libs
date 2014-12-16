"""Kept for backwards compatibility. Please add everything to the path below."""
import warnings

from .utils.s3 import *  # NOQA

warnings.warn('Please import from django_libs.utils.s3 instead.',
              DeprecationWarning)
