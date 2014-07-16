"""
Central definition of all settings used in django-libs.

Devs and contributors, please move or add them here. That will make it easier
to maintain all the default values in the future.

"""
from django.conf import settings


# Default setting for the ``test_email_backend.WhitelistEmailBackend``
# expects tuple of regex. e.g. [r'.*@example.com']
EMAIL_BACKEND_WHITELIST = getattr(settings, 'EMAIL_BACKEND_WHITELIST', [])

# Default setting for the ``test_email_backend.WhitelistEmailBackend``
# if True, it reroutes all the emails, that don't match the
# EMAIL_BACKEND_WHITELIST setting to the emails specified in the
# TEST_EMAIL_BACKEND_RECIPIENTS setting.
EMAIL_BACKEND_REROUTE_BLACKLIST = getattr(settings,
                                          'EMAIL_BACKEND_REROUTE_BLACKLIST',
                                          False)

# Default setting for the ``test_email_backend.EmailBackend``
# format: (('This Name', 'name@example.com'), )       - like the ADMINS setting
TEST_EMAIL_BACKEND_RECIPIENTS = getattr(
    settings, 'TEST_EMAIL_BACKEND_RECIPIENTS', [])


# The default paginate by setting for all comment views
COMMENTS_PAGINATE_BY = getattr(settings, 'COMMENTS_PAGINATE_BY', 10)
