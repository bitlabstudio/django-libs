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

        Set the setting 404_IGNORABLE_USER_AGENTS = []
        Each item can be a regex.

        """
        user_agent = request.META.get('HTTP_USER_AGENT')
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


if _is_ignorable_404:
    from .middleware_1_5 import *  # NOQA
else:
    from .middleware_1_6 import *  # NOQA
