"""Custom middlewares for the project."""
from django.http import HttpResponseRedirect


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
