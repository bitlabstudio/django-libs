Loaders
=======

This module provides a few simple utility functions for loading classes from
strings like ``myproject.models.FooBar``.


load_member_from_setting
------------------------

Use this function to load a member from a setting::

    # in your settings.py:
    FOOBAR_CLASS = 'myproject.models.FooBar'

    # anywhere in your code:
    from django_libs.loaders import load_member_from_settin
    cls = load_member_form_setting('FOOBAR_CLASS')

If you are using the reusable app settings pattern, you can hand in an optional
parameter which should be the ``app_settings`` module where you define your
app's setting's default values::

    # in your app_settings.py:
    from django.conf import settings

    FOOBAR_CLASS = getattr(settings, 'APPNAME_FOOBAR_CLASS', 'appname.models.FooBar')

    # anywhere in your code:
    from appname import app_settings
    from django_libs.loaders import load_member_from_setting

    cls = load_member_from_setting('FOOBAR_CLASS', app_settings)


load_member
-----------

This function is used by ``load_member_from_setting`` internally. Use this
if you already have the FQN string of the member you would like to load::

    # anywhere in your code:
    from django_libs.loaders import load_member

    cls = load_member('myproject.models.FooBar')


split_fqn
---------

This function is used by ``load_member`` internally. Use this if you want
to get the left and right side of a fully qualified name::

    # anywhere in your code:
    from django_libs.loaders import split_fqn

    modulename, classname = split_fqn('myproject.models.FooBar')

In this example, ``modulename`` would be ``myproject.models`` and ``classname``
would be ``FooBar``.
