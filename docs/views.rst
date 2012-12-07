Views
=====

Http404TestView & Http500TestView
---------------------------------

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
