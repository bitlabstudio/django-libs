"""Views for testing 404 and 500 templates."""
from functools import update_wrapper

from django.views.generic import TemplateView, View


class Http404TestView(TemplateView):
    """
    WARNING: This view is deprecated. Use the ``RapidPrototypingView`` instead.

    """
    template_name = '404.html'


class Http500TestView(TemplateView):
    """
    WARNING: This view is deprecated. Use the ``RapidPrototypingView`` instead.

    """
    template_name = '500.html'


class HybridView(View):
    """
    View that renders different views depending on wether the user is authed.

    If the user is authenticated, it will render ``authed_view``, otherwise
    it will render ``anonymous_view``.

    If you are passing in a function based view you can also define
    ``authed_view_kwargs`` and ``anonymous_view_kwargs`` which, of course,
    should be dictionaries.

    """
    authed_view = None
    authed_view_kwargs = None
    anonymous_view = None
    anonymous_view_kwargs = None

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (
                                    cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            self.authed_view = initkwargs.get('authed_view')
            self.authed_view_kwargs = initkwargs.get('authed_view_kwargs')
            self.anonymous_view = initkwargs.get('anonymous_view')
            self.anonymous_view_kwargs = initkwargs.get(
                'anonymous_view_kwargs')
            return self.dispatch(request, *args, **kwargs)
        # take name and docstring from class
        update_wrapper(view, cls, updated=())
        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            view_kwargs = self.authed_view_kwargs or {}
            return self.authed_view(request, **view_kwargs)

        view_kwargs = self.anonymous_view_kwargs or {}
        return self.anonymous_view(request, **view_kwargs)


class RapidPrototypingView(TemplateView):
    """
    View that can render any given template.

    This can be useful when you want your designers to be bale to go ahead and
    create templates although no views have been created for those templates,
    yet.

    """
    def dispatch(self, request, *args, **kwargs):
        self.template_name = kwargs.get('template_path')
        return super(RapidPrototypingView, self).dispatch(request, *args,
                                                          **kwargs)
