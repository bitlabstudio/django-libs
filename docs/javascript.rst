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


modals.js
---------

Provides functions to easily get or post requests that should be shown in a
Twitter Bootstrap modal. In order to use this:

1. Make sure that you are using `bootstrap-modal <https://github.com/jschr/bootstrap-modal/>`_
2. Make sure that you are using the `AjaxRedirectMiddleware <http://django-libs.readthedocs.org/en/latest/middlewares.html#ajaxrequestmiddleware>`_
3. Add `<div id="ajax-modal" class="modal hide fade" tabindex="-1"></div>` at
   the end of your ``base.html``

Now you could place a button somewhere in your code and use the ``onclick``
event to open the modal. You can pass in the URL that serves the modal's
template and extra context that should be sent in the request as GET data::

    <a href="#" onclick="getModal('/ajax-url/', {next: '/profile/'}); return false;">Open Modal</a>

In your modal you might have a form with a submit button. You can now trigger
the POST request like so::

    // This is how your modal template should look like
    <form id="formID" method="post" action="/ajax-url/">
        {% csrf_token %}
        <div class="modal-body">
            <fieldset>
                {% for field in form %}
                    {% include "partials/form_field.html" %}
                {% endfor %}
            </fieldset>
            <input type="hidden" name="next" value="{% if next %}{{ next }}{% endif %}" />
        </div>
        <div class="modal-footer">
            <input type="button" onclick="postModal('/ajax-url/', $('#formID')); return false;" value="Submit">
        </div>
    </form>
