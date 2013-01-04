JavaScript
==========

getcookie.js
------------

Provides the function ``getCookie`` which allows to retrieves values from the
cookie. This is especially useful when you want to do a POST request via
AJAX.

Usage::

    <script src="{{ STATIC_URL }}django_libs/js/getcookie.js"></script>
    <script>
        var data = [{name: 'csrfmiddlewaretoken', value: getCookie('csrftoken')}];
        $.post(
            '/some/url/'
            ,data
            ,function(data) {
                if (data == 'success') {
                    // do something
                }
            }
        );
    </script>
