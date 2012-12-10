"""Custom middlewares for the project."""
from django.http import HttpResponseRedirect


class AjaxRedirectMiddleware(object):
    """
    Middleware that sets a made up status code when a redirect has happened.

    This is necessary for AJAX calls with jQuery. It seems to set the status
    code to 200 when in reality it was a 301 or 302.

    """
    def process_response(self, request, response):
        if request.is_ajax():
            if type(response) == HttpResponseRedirect:
                response.status_code = 278
        return response
