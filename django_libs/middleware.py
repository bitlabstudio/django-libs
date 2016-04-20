"""Custom middlewares for the project."""
from __future__ import absolute_import
import re

from django.conf import settings
from django.core.mail import mail_managers
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text


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
            if request.GET.get('ajax_redirect_passthrough', request.POST.get(
                    'ajax_redirect_passthrough')):
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


class CustomBrokenLinkEmailsMiddleware(object):
    """Custom version that adds the user to the error email."""
    def process_response(self, request, response):
        """
        Send broken link emails for relevant 404 NOT FOUND responses.
        """
        if response.status_code == 404 and not settings.DEBUG:
            domain = request.get_host()
            path = request.get_full_path()
            referer = force_text(
                request.META.get('HTTP_REFERER', ''), errors='replace')

            if not self.is_ignorable_request(request, path, domain, referer):
                ua = request.META.get('HTTP_USER_AGENT', '<none>')
                ip = request.META.get('REMOTE_ADDR', '<none>')

                user = None
                if request.user and hasattr(request.user, 'email'):
                    user = request.user.email
                content = (
                    "Referrer: %s\n"
                    "Requested URL: %s\n"
                    "User agent: %s\n"
                    "IP address: %s\n"
                    "User: %s\n"
                ) % (referer, path, ua, ip, user)
                if self.is_internal_request(domain, referer):
                    internal = 'INTERNAL '
                else:
                    internal = ''
                mail_managers(
                    "Broken %slink on %s" % (
                        internal,
                        domain
                    ),
                    content,
                    fail_silently=True)
        return response

    def is_internal_request(self, domain, referer):
        """
        Returns True if referring URL is the same domain as current request.

        """
        # Different subdomains are treated as different domains.
        return bool(re.match("^https?://%s/" % re.escape(domain), referer))

    def is_ignorable_request(self, request, uri, domain, referer):
        """
        Returns True if the given request *shouldn't* notify the site managers.
        """
        # '?' in referer is identified as search engine source
        if (not referer or (not self.is_internal_request(
                domain, referer) and '?' in referer)):
            return True
        return any(
            pattern.search(uri) for pattern in settings.IGNORABLE_404_URLS)
