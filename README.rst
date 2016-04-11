Django Libs
===========

This project aims to provide commonly used building blocks for Django projects
and applications.

**Current features**:

* TestCase mixins to ease the process of testing views via ``self.client.get``
* A JSONResponseMixin
* New generic class based view DetailViewWithPostAction which is able to
  handle custom post actions.
* Template filter to provide field's verbose names
* Template tag for displaying the currently selected main navigation item
* Custom test_email_backend that sends emails to your own address no matter
  who the recepient is
* Functions to test callable or non-callable views
* Dummy views to test your 404 and 500 templates
* RapidPrototypingView to render any template even when it has no view hooked
  up in ``urls.py``.
* AjaxRedirectMiddleware for jQuery AJAX calls that return 301 redirects
* AjaxResponseMixin for views that can return their normal template or a
  partial template when it is an ajax call
* AccessMixin which allows to use views with the ``login_required`` decorator
  based on a setting.
* A context processor to add your analytics tracking code to your template
  context.
* A decorator ``lockfile`` for wrapping ``handle`` methods of admin commands
  so that they never run twice at the same time.
* A ``getCookie`` js function that can be used to retrieve the csrf token
  for AJAX POST requests.
* A templatetag ``call`` which allows to call any method with params.
* Utilities for loading classes from a string like ``myproject.models.Foobar``.
* Form, which add field labels as placeholder attributes.
* Function to convert html code into formatted plain text.
* Amazon S3 storage + django-compressor support files.
* An AJAX View to display paginated comments for every possible object.
* Tools to improve django-hvad

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
