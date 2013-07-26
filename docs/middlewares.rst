Middlewares
===========

AjaxRedirectMiddleware
----------------------

When calling a view from an AJAX call and when that view returns a redirect,
jQuery changes the status code to 200. This means, in your success callback
you will not be able to determine, if the view returned to 200 or a redirect.

Interestingly, there is a workaround: If we return some made up status code,
jQuery will not change it.

This middleware makes sure that, if there was a redirect and if it was an
AJAX call, the return code will be set to ``278``.

In order to use this middleware, add it to your ``MIDDLEWARE_CLASSES``
setting::

    MIDDLEWARE_CLASSES = [
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        ...
        'django_libs.middleware.AjaxRedirectMiddleware',
    ]


In your jQuery script you can now react to redirects::

    $.post(url, data, function(data, textStatus, jqXHR) {
        if (jqXHR.status == 278) {
            window.location.href = jqXHR.getResponseHeader("Location");
        } else {
            $("#" + container).replaceWith(data);
        }
    });
