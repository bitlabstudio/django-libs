Test Email Backend
==================

EmailBackend
------------

``EmailBackend`` is a simple Email backend, that sends all emails to a defined
address, no matter what the recipient really is.

This is useful in times of development & testing to prevent mass mails to
example.com or existing addresses and to review all email communication.

In order to use it, set this in your local_settings.py::

    EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'
    TEST_EMAIL_BACKEND_RECIPIENTS = (
        ('Name', 'email@gmail.com'),
    )

If you're using django-mailer don't forget to add::

    MAILER_EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'


WhitelistEmailBackend
---------------------

``WhitelistEmailBackend`` provides more control over what can be sent where.

To use it, first define the ``EMAIL_BACKEND_WHITELIST`` setting:::

    EMAIL_BACKEND_WHITELIST = [r'.*@example.com']

This setting holds regex patterns which define, which emails may be sent and
which are being discarded. The above example will allow every email adress from
the ``example.com`` domain to be delivered.

If you still want to receive all the discarded emails, you can additionally
define ``TEST_EMAIL_BACKEND_RECIPIENTS`` like above and set
``EMAIL_BACKEND_REROUTE_BLACKLIST`` to ``True``::

    EMAIL_BACKEND_REROUTE_BLACKLIST = True
    TEST_EMAIL_BACKEND_RECIPIENTS = (
        ('Name', 'email@gmail.com'),
    )

With this setup, all recipients, that match one of the whitelisted email
patterns will be sent to the correct recipient, but in case it didn't match,
the recipients will be replaced with the ones from the
``TEST_EMAIL_BACKEND_RECIPIENTS`` setting.
