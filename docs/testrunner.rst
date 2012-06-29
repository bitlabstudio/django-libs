Testrunner
==========

We like to combine django-nose (https://github.com/jbalogh/django-nose) and
django-coverage (https://github.com/kmike/django-coverage) to create a custom
testrunner that uses Nose for test file discovery and generates a coverage
report on each test run.

The reason why we use nose is that we can easily exclude folders containing
test files, for example slow integration tests.

Installation
------------

Create a ``test_settings.py`` in your project with the following code::

    from myproject.settings import *
    from django_libs.settings.test_settings import *

We assume that you are using the new project layout that comes with Django 1.4
where your ``settings.py`` lives inside the ``myproject`` folder.

In order for this to work you should split up your ``INSTALLED_APPS`` setting
into several lists. This allows us to tell coverage to ignore all external apps
in the coverage report because we don't run tests of external apps::

    INTERNAL_APPS = [
        'myproject',
        'foobar',
    ]

    EXTERNAL_APPS = [
        'cms',
        'shop',
    ]

    DJANGO_APPS = [
        ...
    ]

    INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + INTERNAL_APPS

You will probably want to add ``coverage/`` to your ``.gitignore`` file.

Usage
-----

Run your tests with your new ``test_settings.py``::

    ./manage.py test -v 2 --traceback --failfast --settings=myproject.test_settings

Or if you want to exclude integration tests::

    ./manage.py test -v 2 --traceback --failfast --settings=myproject.test_settings --exclude='integration_tests'

You will probably want to write a Fabric task ``fab test`` to make this call
a bit more convenient.
