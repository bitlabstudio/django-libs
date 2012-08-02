"""Useful mixins for class based views."""
import json

from django.http import HttpResponse


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
