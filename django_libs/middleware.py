"""Custom middlewares for the project."""
from __future__ import absolute_import
import re

from django.conf import settings
from django.http import HttpResponseRedirect

try:
    from django.middleware.common import _is_ignorable_404
except ImportError:
    _is_ignorable_404 = None


class AjaxRedirectMiddleware(object):
    """
    Middleware that sets a made up status code when a redirect has happened.

    This is necessary for AJAX calls with jQuery. It seems to set the status
    code to 200 when in reality it was a 301 or 302.

    If you want to override this behaviour for some of your ajax calls, you
    can add `ajax_redirect_passthrough` as a hidden field or as a GET
    parameter.

    """
    def process_response(self, request, response):
        if request.is_ajax():
            if (request.GET.get('ajax_redirect_passthrough')
                    or request.POST.get('ajax_redirect_passthrough')):
                return response
            if type(response) == HttpResponseRedirect:
                response.status_code = 278
        return response


class CustomSentry404CatchMiddleware(object):
    """Same as original middleware but can ignore given user agents."""
    def is_ignorable_user_agent(self, request):
        """
        Returns ``True`` if the user agent is in the list of ignored agents.

        Set the setting RAVEN_404_IGNORABLE_USER_AGENTS = []
        Each item can be a regex.

        """
        from user_agents import parse
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ua = parse(user_agent)

        ignore_spiders = getattr(settings, 'RAVEN_IGNORE_SPIDERS', True)
        if ignore_spiders and ua.device.family == 'Spider':
            return True

        ignorable_agents = getattr(settings, 'RAVEN_IGNORABLE_USER_AGENTS', [])
        for ignorable_agent in ignorable_agents:
            result = re.match(ignorable_agent, user_agent)
            if result:
                return True
        return False

    def process_response(self, request, response):
        if self.is_ignorable_user_agent(request):
            return response

        from raven.contrib.django.middleware import Sentry404CatchMiddleware
        sentry_middleware = Sentry404CatchMiddleware()
        return sentry_middleware.process_response(request, response)


class ErrorMiddleware(object):
    """Alter HttpRequest objects on Error."""

    def process_exception(self, request, exception):
        """
        Add user details.
        """
        if request.user and hasattr(request.user, 'email'):
            request.META['USER'] = request.user.email


class SSLRedirect:
    """
    Redirects all non-SSL requests to the SSL versions.

    You can add exceptions via the setting ``NO_SSL_URLS``. This allows you to
    forward your whole website to the SSL version except for a few URLs that
    you need to serve via non-SSL for whatever reason.

    """
    def process_request(self, request):
        no_ssl_urls = getattr(settings, 'NO_SSL_URLS', [])
        urls = tuple([re.compile(url) for url in no_ssl_urls])

        secure = False
        for url in urls:
            if not url.match(request.path):
                secure = True
                break
        if not secure == self._is_secure(request):
            return self._redirect(request, secure)

    def _is_secure(self, request):
        if request.is_secure():
            return True

        # Handle the Webfaction case until this gets resolved in the
        # request.is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

        return False

    def _redirect(self, request, secure):
        protocol = secure and "https" or "http"
        if secure:
            host = getattr(settings, 'SSL_HOST', request.get_host())
        else:
            host = getattr(settings, 'HTTP_HOST', request.get_host())
        newurl = "%s://%s%s" % (protocol, host, request.get_full_path())
        if settings.DEBUG and request.method == 'POST':
            raise Exception(
                "Django can't perform a SSL redirect while maintaining POST"
                " data. Please structure your views so that redirects only"
                " occur during GETs.")

        return HttpResponseRedirect(newurl)


if _is_ignorable_404:
    from .middleware_1_5 import *  # NOQA
else:
    from .middleware_1_6 import *  # NOQA
