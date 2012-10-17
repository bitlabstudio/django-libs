"""Useful mixins for class based views."""
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView


class DetailViewWithPostAction(DetailView):
    """
    Generic class based view to handle custom post actions in a DetailView.

    When you derive from this class, your buttons need to be called
    `post_actionname` and you have to implement action handlers with the
    name `post_actionname` and url retrievers with the name
    `get_success_url_post_actionname`.

    If all actions should have the same success url, you can also implement
    `get_success_url`, which will be used as a fallback in case that no
    specific url retrieve has been implemented.

    """
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        for key in self.request.POST.keys():
            if key.startswith('post_'):
                getattr(self, key)()
                break
        success_url_handler = getattr(self, 'get_success_url_%s' % key, False)
        if not success_url_handler:
            success_url_handler = getattr(self, 'get_success_url')
        success_url = success_url_handler()
        return HttpResponseRedirect(success_url)


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.

    Taken from here: https://docs.djangoproject.com/en/dev/topics/class-based-views/#more-than-just-html

    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.

        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        """
        Convert the context dictionary into a JSON object.

        If your context has complex Django objects, you need to override this
        method and make sure that the context gets transformed into something
        that ``json.dumps`` can handle.

        """
        return json.dumps(context)
