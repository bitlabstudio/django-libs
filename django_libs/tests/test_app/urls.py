"""URLs for the test app."""
from django.urls import path, re_path
from django.http import HttpResponse
from django.views.generic import View

from django_libs import views

View.get = lambda req, *args, **kwargs: HttpResponse('SUCCESS!')
authed_view = View.as_view()
authed_view_kwargs = {'authed': True}
anonymous_view = View.as_view()
anonymous_view_kwargs = {'anonymous': True}


urlpatterns = [
    path('', views.HybridView.as_view(
        authed_view=authed_view,
        authed_view_kwargs=authed_view_kwargs,
        anonymous_view=anonymous_view,
        anonymous_view_kwargs=anonymous_view_kwargs),
        name='dummy_hybrid'),
    path('update-session/', views.UpdateSessionAJAXView.as_view(), name='update_session'),
    path('update-cookie/', views.UpdateCookieAJAXView.as_view(), name='update_cookie'),
    re_path(r'^prototype/(?P<template_path>.*)$', views.RapidPrototypingView.as_view(), name='prototype'),
]
