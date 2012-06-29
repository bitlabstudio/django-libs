Django Libs
===========

This project aims to provide commonly used building blocks for Django projects
and applications.

Here are some things that this project provides:

* A custom testrunner that uses django-nose for discovering tests and
  django-coverage for automatically generating a coverage report on each test
  run
* A factory for creating User objects

Installation
------------

To get the latest stable release from PyPi::

    $ pip install django-libs

To get the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-libs.git#egg=django_libs

Usage
-----

See the docs folder for descriptions of the different tools this project
provides.

Or read the docs here: http://django-libs.readthedocs.org/en/latest/

Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-libs
    $ pip install -r requirements.txt

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch
