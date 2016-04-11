Utils Email
===========

send_email
----------

``send_email`` sends html emails based on templates for subject and body.

Please note that ``protocol`` and ``domain`` variables have already been
placed in the context.

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
        reply_to='foo@example.com',
    )
