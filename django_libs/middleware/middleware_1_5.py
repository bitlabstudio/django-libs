"""Custom middleware for Django 1.5 projects."""
import hashlib

from django import http
from django.conf import settings
from django.core.mail import mail_managers
from django.middleware.common import (
    CommonMiddleware,
    _is_ignorable_404,
    _is_internal_request,
)


class CustomCommonMiddleware(CommonMiddleware):
    """Adds the current user to the 405 email."""
    def process_response(self, request, response):
        "Send broken link emails and calculate the Etag, if needed."
        if response.status_code == 404:
            if settings.SEND_BROKEN_LINK_EMAILS and not settings.DEBUG:
                # If the referrer was from an internal link or a
                # non-search-engine site, send a note to the managers.
                domain = request.get_host()
                referer = request.META.get('HTTP_REFERER')
                is_internal = _is_internal_request(domain, referer)
                path = request.get_full_path()
                if (referer
                        and not _is_ignorable_404(path)
                        and (is_internal or '?' not in referer)):
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
                    ) % (referer, request.get_full_path(), ua, ip, user)
                    internal = is_internal and 'INTERNAL ' or ''
                    mail_managers(
                        "Broken %slink on %s" % (internal, domain),
                        content,
                        fail_silently=True,
                    )
                return response

        # Use ETags, if requested.
        if settings.USE_ETAGS:
            if response.has_header('ETag'):
                etag = response['ETag']
            elif response.streaming:
                etag = None
            else:
                etag = '"%s"' % hashlib.md5(response.content).hexdigest()
            if etag is not None:
                if (200 <= response.status_code < 300
                        and request.META.get('HTTP_IF_NONE_MATCH') == etag):
                    cookies = response.cookies
                    response = http.HttpResponseNotModified()
                    response.cookies = cookies
                else:
                    response['ETag'] = etag

        return response
