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



PaginatedCommentAJAXView
------------------------

Provides a simple solution to display comments from the Django comment
framework for any object. It's paginated and because it uses ajax, there's no
need to reload the page every time you want to change a page.

Hook up the view in your urls:::

    from django_libs.views import PaginatedCommentAJAXView

    urlpatterns += patterns(
        '',
        ...
        url(r'^comments/$', PaginatedCommentAJAXView.as_view(),
            name='libs_comment_ajax'),
    )


Add the comment scripts. E.g. in your ``base.html`` do:::

    {% load static %}

    <script type="text/javascript" src="{% static "django_libs/js/comments.js" %}"></script>


Add the markup to the template, that contains the object, you want to display
comments for:::

    <div data-id="ajaxComments" data-ctype="mymodel" data-object-pk="{{ object.pk }}" data-comments-url="{% url "libs_comment_ajax" %}"></div>


* ``data-id=ajaxComments`` indicates to the scripts, that inside this div is
  where to render the comment list template.
* ``data-ctype`` is the content type name of the object. E.g. 'user' for
  ``auth.User``.
* ``data-object-pk`` is most obiously the object's primary key.
* ``data-comments-url`` is the url you've hooked up the view.

To customize the template take a look at ``django_libs/templates/django_libs/partials/ajax_comments.html``.

Also you can choose the amount of comments per page via the setting
``COMMENTS_PAGINATE_BY``:::

    COMMENTS_PAGINATE_BY = 10  # default

There you go. All done.



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
---------------------

This view allows you to update any session variables in an AJAX post.

In order to use this view, hook it up in your ``urls.py``::

    from django_libs.views import UpdateSessionAJAXView
    urlpatterns += patterns(
        '',
        url(r'^update-session/$', UpdateSessionAJAXView.as_view(),
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
