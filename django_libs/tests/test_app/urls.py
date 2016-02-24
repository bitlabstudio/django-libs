"""URLs for the test app."""
from django.conf.urls import url
from django.http import HttpResponse
from django.views.generic import View

from django_libs import views

View.get = lambda req, *args, **kwargs: HttpResponse('SUCCESS!')
authed_view = View.as_view()
authed_view_kwargs = {'authed': True}
anonymous_view = View.as_view()
anonymous_view_kwargs = {'anonymous': True}


urlpatterns = [
    url(r'^$', views.HybridView.as_view(
        authed_view=authed_view,
        authed_view_kwargs=authed_view_kwargs,
        anonymous_view=anonymous_view,
        anonymous_view_kwargs=anonymous_view_kwargs),
        name='dummy_hybrid'),
    url(r'^update-session/$', views.UpdateSessionAJAXView,
        name='update_session'),
    url(r'^update-cookie/$', views.UpdateCookieAJAXView,
        name='update_cookie'),
    url(r'^prototype/(?P<template_path>.*)$',
        views.RapidPrototypingView.as_view(),
        name='prototype'),
]
