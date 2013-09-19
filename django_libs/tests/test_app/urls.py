"""URLs for the test app."""
from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse
from django.views.generic import View

from django_libs.views import HybridView

View.get = lambda req, *args, **kwargs: HttpResponse('SUCCESS!')
authed_view = View.as_view()
authed_view_kwargs = {'authed': True}
anonymous_view = View.as_view()
anonymous_view_kwargs = {'anonymous': True}


urlpatterns = patterns(
    '',
    url(r'^$', HybridView.as_view(
        authed_view=authed_view,
        authed_view_kwargs=authed_view_kwargs,
        anonymous_view=anonymous_view,
        anonymous_view_kwargs=anonymous_view_kwargs,
        ), name='dummy_hybrid'),
)
