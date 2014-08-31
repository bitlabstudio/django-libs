"""Useful mixins for class based views."""
import json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView


class AccessMixin(object):
    """Mixin to controls access to the view based on a setting."""
    access_mixin_setting_name = None

    def dispatch(self, request, *args, **kwargs):
        # Check, if user needs to be logged in
        if self.access_mixin_setting_name is None:
            raise Exception(
                'Please set `access_mixin_setting_name` on the view that'
                ' inherits the AccessMixin')
        if getattr(settings, self.access_mixin_setting_name, False):
            return super(AccessMixin, self).dispatch(
                request, *args, **kwargs)
        return login_required(super(AccessMixin, self).dispatch)(
            request, *args, **kwargs)


class AjaxResponseMixin(object):
    """
    A mixin that prepends `ajax_` to the template name when it is an ajax call.

    This gives you the chance to return partial templates when it is an ajax
    call, so you can render the output inside of a modal, for example.

    """
    ajax_template_prefix = 'ajax_'

    def get_template_names(self):
        names = super(AjaxResponseMixin, self).get_template_names()
        if self.request.is_ajax():
            count = 0
            for name in names:
                filename_split = list(os.path.split(name))
                old_filename = filename_split[-1]
                new_filename = '{0}{1}'.format(
                    self.ajax_template_prefix, old_filename)
                filename_split[-1] = new_filename
                names[count] = os.path.join(*filename_split)
                count += 1
        return names


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

    Taken from here: https://docs.djangoproject.com/en/dev/topics/
    class-based-views/#more-than-just-html

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
