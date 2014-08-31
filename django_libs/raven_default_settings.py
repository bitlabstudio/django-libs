"""Default settings for the CustomRaven404CatchMiddleware"""
import warnings

from . import default_settings

warnings.warn(
    'This setting is deprecated.'
    ' Please import from django_libs.default_settings instead.',
    DeprecationWarning)

# NOTE: kept for backwards compatibility. Default setting should always be
# defined in ``default_settings.py``
RAVEN_IGNORABLE_USER_AGENTS = \
    default_settings.RAVEN_IGNORABLE_USER_AGENTS_DEFAULT