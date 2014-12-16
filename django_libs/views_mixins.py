"""Kept for backwards compatibility. Please add everything to the path below."""
import warnings

from .views.mixins import *  # NOQA

warnings.warn('Please import from django_libs.views.mixins instead.',
              DeprecationWarning)
