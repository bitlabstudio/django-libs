"""Custom middlewares for the project."""
import hashlib

from django import http
from django.conf import settings
from django.core.mail import mail_managers
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
    from .middleware_1_6 import *
