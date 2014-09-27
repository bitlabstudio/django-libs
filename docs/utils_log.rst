Utils Log
=========

AddCurrentUser
--------------

This logging filter adds the current user's email to the request's META dict.
This way the user will show up in the traceback that is sent via email by
Django's logging framework.

Add it to your logging settings like so::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            ...
            'add_current_user': {
                '()': 'django_libs.utils_log.AddCurrentUser'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'WARNING',
                'filters': [
                    ...
                    'add_current_user', ],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            ...
        },
        ...


FilterIgnorable404URLs
----------------------

This logging filter allows you to ignore 404 logging for certain URLs and for
certain user agents.

Define the list of ignorable URLs like so::

    IGNORABLE_404_URLS = [
        re.compile(r'\.php/?$', re.I),
        re.compile(r'\'/?$', re.I),
        re.compile(r'^/assets/'),
    ]

Define the list of ignorable user agents like so::

   IGNORABLE_404_USER_AGENTS = [
        re.compile(r'FacebookBot', re.I),
        re.compile(r'Googlebot', re.I),
        re.compile(r'Mail.RU_Bot', re.I),
        re.compile(r'Twitterbot', re.I),
        re.compile(r'bingbot', re.I),
        ...
    ]

Then add the logging filter to your logging settings::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            ...
            'filter_ignorable_404_urls': {
                '()': 'django_libs.utils_log.FilterIgnorable404URLs'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'WARNING',
                'filters': [
                    ...
                    'filter_ignorable_404_urls',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            ...
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'WARNING',
                'propagate': True,
            },
            ...
        }
    }

NOTE: Make sure to set the log level for the `mail_admins` handler and for
the loggers that use this handler to `WARNING`, otherwise 404 emails will not
be sent.
