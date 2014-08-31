"""Default settings for the CustomRaven404CatchMiddleware"""
from . import default_settings

# NOTE: kept for backwards compatibility. Default setting should always be
# defined in ``default_settings.py``
RAVEN_IGNORABLE_USER_AGENTS = \
    default_settings.RAVEN_IGNORABLE_USER_AGENTS_DEFAULT