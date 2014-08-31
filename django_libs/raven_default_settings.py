"""Default settings for the CustomRaven404CatchMiddleware"""
from . import default_settings

raise DeprecationWarning(
    'This setting is deprecated.'
    ' Please import from django_libs.default_settings instead.')

# NOTE: kept for backwards compatibility. Default setting should always be
# defined in ``default_settings.py``
RAVEN_IGNORABLE_USER_AGENTS = \
    default_settings.RAVEN_IGNORABLE_USER_AGENTS_DEFAULT