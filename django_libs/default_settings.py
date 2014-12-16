"""
Central definition of all settings used in django-libs.

Devs and contributors, please move or add them here. That will make it easier
to maintain all the default values in the future.

"""
from django.conf import settings


# The default paginate by setting for all comment views
COMMENTS_PAGINATE_BY = getattr(settings, 'COMMENTS_PAGINATE_BY', 10)

CUSTOM_FORMAT_MODULE_PATHS = getattr(settings, 'CUSTOM_FORMAT_MODULE_PATHS',
                                     ['localized_names.formats'])

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

NO_SSL_URLS = getattr(settings, 'NO_SSL_URLS', [])

# Default setting for the ``test_email_backend.EmailBackend``
# format: (('This Name', 'name@example.com'), )       - like the ADMINS setting
TEST_EMAIL_BACKEND_RECIPIENTS = getattr(
    settings, 'TEST_EMAIL_BACKEND_RECIPIENTS', [])


RAVEN_IGNORE_SPIDERS = getattr(settings, 'RAVEN_IGNORE_SPIDERS', True)
RAVEN_IGNORABLE_USER_AGENTS_DEFAULT = [
    r'AhrefsBot',
    r'EasouSpider',
    r'FacebookBot',
    r'Feedfetcher-Google',
    r'Googlebot',
    r'Mail.RU_Bot',
    r'Test Certificate Info',
    r'Twitterbot',
    r'Yahoo! Slurp',
    r'YandexBot',
    r'bingbot',
]
RAVEN_IGNORABLE_USER_AGENTS = getattr(
    settings, 'RAVEN_IGNORABLE_USER_AGENTS', RAVEN_IGNORABLE_USER_AGENTS_DEFAULT
)


# HTML2PlainParser settings ====================================================
HTML2PLAINTEXT_IGNORED_ELEMENTS = getattr(
    settings, 'HTML2PLAINTEXT_IGNORED_ELEMENTS',
    ['html', 'head', 'style', 'meta', 'title', 'img']
)
HTML2PLAINTEXT_NEWLINE_BEFORE_ELEMENTS = getattr(
    settings, 'HTML2PLAINTEXT_NEWLINE_BEFORE_ELEMENTS',
    ['br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'li']
)
HTML2PLAINTEXT_NEWLINE_AFTER_ELEMENTS = getattr(
    settings, 'HTML2PLAINTEXT_NEWLINE_AFTER_ELEMENTS',
    ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'td']
)
HTML2PLAINTEXT_STROKE_BEFORE_ELEMENTS = getattr(
    settings, 'HTML2PLAINTEXT_STROKE_BEFORE_ELEMENTS',
    ['tr']
)
HTML2PLAINTEXT_STROKE_AFTER_ELEMENTS = getattr(
    settings, 'HTML2PLAINTEXT_STROKE_AFTER_ELEMENTS',
    ['tr']
)
HTML2PLAINTEXT_STROKE_TEXT = getattr(
    settings, 'HTML2PLAINTEXT_STROKE_TEXT', '------------------------------\n')
