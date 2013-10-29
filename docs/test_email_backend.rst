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
