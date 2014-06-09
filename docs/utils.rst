Utils
=====

conditional_decorator
---------------------

Allows you to decorate a function based on a condition.

This can be useful if you want to require login for a view only if a certain
setting is set::

    from django.conf import settings
    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator
    from django_libs.utils import conditional_decorator
    class MyView(ListView):
        @conditional_decorator(method_decorator(login_required), settings.LOGIN_REQUIRED)
        def dispatch(self, request, *args, **kwargs):
            return super(MyView, self).dispatch(request, *args, **kwargs)


create_random_string
--------------------

Returns a random string. By default it returns 7 unambiguous capital letters
and numbers, without any repetitions::

    from django_libs.utils import create_random_string

    result = create_random_string()

Will return something like ``CH178AS``.
You can set a length, characters to use and you can allow repetitions::

    result = create_random_string(length=3, chars='abc123', repetitions=True)


html_to_plain_text
------------------

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
+++++++++++++++++++++++++++++++

Default: ['html', 'head', 'style', 'meta', 'title', 'img']

Put any tags in here, which should be ignored in the converting process.


HTML2PLAINTEXT_NEWLINE_BEFORE_ELEMENTS
++++++++++++++++++++++++++++++++++++++

Default: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'li']

Put any tags in here, which should get a linebreak in front of their content.


HTML2PLAINTEXT_NEWLINE_AFTER_ELEMENTS
+++++++++++++++++++++++++++++++++++++

Default: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'td']

Put any tags in here, which should get a linebreak at the end of their content.


HTML2PLAINTEXT_STROKE_BEFORE_ELEMENTS
+++++++++++++++++++++++++++++++++++++

Default: ['tr']

Put any tags in here, which should get a stroke in front of their content.


HTML2PLAINTEXT_STROKE_AFTER_ELEMENTS
++++++++++++++++++++++++++++++++++++

Default: ['tr']

Put any tags in here, which should get a stroke at the end of their content.


HTML2PLAINTEXT_STROKE_TEXT
++++++++++++++++++++++++++

Default: '------------------------------\n'

You can override the appearance of a stroke.
