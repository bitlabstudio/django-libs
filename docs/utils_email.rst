Utils Email
===========

send_email
----------

``send_email`` sends html emails via django-mailer based on templates for
subject and body.

+----------------------+----------------------------------------------------+
| Argument             | Definition                                         |
+======================+====================================================+
| ``request``          | The current request instance.                      |
+----------------------+----------------------------------------------------+
| ``extra_context``    | A dictionary of items that should be added to      |
|                      | the templates' contexts                            |
+----------------------+----------------------------------------------------+
| ``subject_template`` | A string representing the path to the template of  |
|                      | of the email's subject.                            |
+----------------------+----------------------------------------------------+
| ``body_template``    | A string representing the path to the template of  |
|                      | the email's body.                                  |
+----------------------+----------------------------------------------------+
| ``from_email``       | String that represents the sender of the email.    |
+----------------------+----------------------------------------------------+
| ``recipients``       | A tuple of recipients.                             |
+----------------------+----------------------------------------------------+

In order to use it, include the following code::

    send_email(
        request={},
        extra_context={'Foo': bar},
        subject_template='email/notification_subject.html',
        body_template='email/notification_body.html',
        from_email=('Name', 'email@gmail.com'),
        recipients=[self.user.email, ]
    )
