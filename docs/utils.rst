Utils
=====

Converter
---------

html_to_plain_text
++++++++++++++++++

Converts html code into formatted plain text.

Use it to e.g. provide an additional plain text email.

Just feed it with some html::

    from django_libs.utils import html_to_plain_text

    html = (
        """
        <html>
                <head></head>
                <body>
                    <ul>
                        <li>List element</li>
                        <li>List element</li>
                        <li>List element</li>
                    </ul>
                </body>
            </html>
        """
    )
    plain_text = html_to_plain_text(html)

This will result in::

    * List element
    * List element
    * List element

You can also feed the parser with a file::

    from django_libs.utils import html_to_plain_text

    with open('test_app/templates/html_email.html', 'rb') as file:
        plain_text = html_to_plain_text(file)

You can customize this parser by overriding its settings:

HTML2PLAINTEXT_IGNORED_ELEMENTS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default: ['html', 'head', 'style', 'meta', 'title', 'img']

Put any tags in here, which should be ignored in the converting process.


HTML2PLAINTEXT_NEWLINE_BEFORE_ELEMENTS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'li']

Put any tags in here, which should get a linebreak in front of their content.


HTML2PLAINTEXT_NEWLINE_AFTER_ELEMENTS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'td']

Put any tags in here, which should get a linebreak at the end of their content.


HTML2PLAINTEXT_STROKE_BEFORE_ELEMENTS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default: ['tr']

Put any tags in here, which should get a stroke in front of their content.


HTML2PLAINTEXT_STROKE_AFTER_ELEMENTS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default: ['tr']

Put any tags in here, which should get a stroke at the end of their content.


HTML2PLAINTEXT_STROKE_TEXT
^^^^^^^^^^^^^^^^^^^^^^^^^

Default: '------------------------------\n'

You can override the appearance of a stroke.


Decorators
----------

conditional_decorator
^^^^^^^^^^^^^^^^^^^^^

Allows you to decorate a function based on a condition.

This can be useful if you want to require login for a view only if a certain
setting is set::

    from django.conf import settings
    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator

    from django_libs.utils import conditional_decorator


    class MyView(ListView):
        @conditional_decorator(method_decorator(login_required),
                               settings.LOGIN_REQUIRED)
        def dispatch(self, request, *args, **kwargs):
            return super(MyView, self).dispatch(request, *args, **kwargs)


Email
-----

send_email
++++++++++

``send_email`` sends html emails based on templates for subject and body.

Please note that ``protocol`` and ``domain`` variables have already been
placed in the context. You are able to easily build links::

    <a href="{{ protocol }}{{ domain }}{% url "home" %}">Home</a>

Have a look at the docstrings in the code for further explanations:
https://github.com/bitmazk/django-libs/blob/master/django_libs/utils_email.py

In order to use it, include the following code::

    send_email(
        request={},
        context={'Foo': bar},
        subject_template='email/notification_subject.html',
        body_template='email/notification_body.html',
        from_email=('Name', 'email@gmail.com'),
        recipients=[self.user.email, ],
        reply_to='foo@example.com',  # optional
    )

If you want to add additional context variables you can use the following
setting:

    DJANGO_LIBS_EMAIL_CONTEXT = 'path.to.context_function'

The relevant function should allow a request parameter:

    def context_function(request):
        return {
            'foo': 'bar',
        }

Log
---

AddCurrentUser
^^^^^^^^^^^^^^

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
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'WARNING',
                'filters': [
                    ...
                    'add_current_user',
                ],
                'class': 'django.utils.log.AdminEmailHandler'
            },
        },
        ...
    }


FilterIgnorable404URLs
----------------------

This logging filter allows you to ignore 404 logging for certain URLs and for
certain user agents.

We've already prepared some URLs and user agents. You might want to add them
to your settings::

    from django_libs.settings.django_settings import *  # NOQA

Alternatively, you can extend those lists or write your own.

How to define your own list of ignorable URLs::

    IGNORABLE_404_URLS = [
        re.compile(r'\.php/?$', re.I),
        re.compile(r'\'/?$', re.I),
        re.compile(r'^/assets/'),
        ...
    ]

How to define your list of ignorable user agents::

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
                ],
                'class': 'django.utils.log.AdminEmailHandler'
            },
        },
        ...
    }

NOTE: Make sure to set the log level for the `mail_admins` handler and for
the loggers that use this handler to `WARNING`, otherwise 404 emails will not
be sent.

Text
----

create_random_string
^^^^^^^^^^^^^^^^^^^^

Returns a random string. By default it returns 7 unambiguous capital letters
and numbers, without any repetitions::

    from django_libs.utils import create_random_string

    result = create_random_string()

Will return something like ``CH178AS``.
You can set a length, characters to use and you can allow repetitions::

    result = create_random_string(length=3, chars='abc123', repetitions=True)
