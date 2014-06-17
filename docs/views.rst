Views
=====

Http404TestView & Http500TestView
---------------------------------

Warning: These views are deprecated. Use the ``RapidPrototypingView`` instead.

Simple template views that use the ``404.html`` and ``500.html`` template.
Just create this template in your project's `templates`` folder and add the
views to your ``urls.py``::

    from django_libs.views import Http404TestView, Http500TestView
    urlpatterns += patterns(
        '',
        url(r'^404/$', Http404TestView.as_view()),
        url(r'^500/$', Http500TestView.as_view()),
        ...
    )


HybridView
----------

You often need to display a different home page for authenticated users. For
example Facebook shows a login page when you visit their site but when you
are logged in it shows your stream under the same URL.

This ``HybridView`` does the same thing. Here is how you use it in your
``urls.py``::

    from django_libs.views import HybridView
    from myapp.views import View1
    from myapp2.views import func_based_view

    authed_view = View1.as_view(template_name='foo.html')
    anonymous_view = func_based_view
    anonymous_view_kwargs = {'template_name': 'bar.html', }

    urlpatterns += patterns(
        '',
        ...
        url(r'^$',
            HybridView.as_view(
                authed_view=authed_view, anonymous_view=anonymous_view,
                anonymous_view_kwargs=anonymous_view_kwargs
            ),
        name='home',
    )


RapidPrototypingView
--------------------

This view allows you to render any template even when there is no URL hooked
up and no view implemented. This allows your designers to quickly start writing
HTML templates even before your developers have created views for those
templates.

In order to use this view, hook it up in your ``urls.py``::

    from django_libs.views import RapidPrototypingView
    urlpatterns += patterns(
        '',
        url(r'^prototype/(?P<template_path>.*)$',
            RapidPrototypingView.as_view(),
            name='prototype')
        ...
    )

Now you can call any template by adding it's path to the URL of the view::

    localhost:8000/prototype/404.html
    localhost:8000/prototype/cms/partials/main_menu.html

Check out the ``load_context`` templatetag which allos you to create fake
context variables for your template.


UpdateSessionAJAXView
--------------------

This view allows you to update any session variables in an AJAX post.

In order to use this view, hook it up in your ``urls.py``::

    from django_libs.views import UpdateSessionAJAXView
    urlpatterns += patterns(
        '',
        url(r'^update-session/$', UpdateSessionAJAXView,
            name='update_session'),
        ...
    )

Now you can call it by using ``session_name`` and ``session_value``::

    <script src="{% static "django_libs/js/getcookie.js" %}"></script>
    <script>
        var data = [
            {name: 'csrfmiddlewaretoken', value: getCookie('csrftoken')}
            ,{name: 'session_name', value: 'foo'}
            ,{name: 'session_value', value: 'bar'}
        ];
        $.post(
            '/update-session/'
            ,data
        );
    </script>
