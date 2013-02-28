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
    """View that renders view1 if user is authenticated, otherwise view2."""
    view1 = None
    view1_kwargs = None
    view2 = None
    view2_kwargs = None

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
                                "attributes of the class." % (cls.__name__, key))
        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            self.view1 = initkwargs.get('view1')
            self.view1_kwargs = initkwargs.get('view1_kwargs')
            self.view2 = initkwargs.get('view2')
            self.view2_kwargs = initkwargs.get('view2_kwargs')
            return self.dispatch(request, *args, **kwargs)
        # take name and docstring from class
        update_wrapper(view, cls, updated=())
        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            view_kwargs = self.view1_kwargs or {}
            return self.view1(request, **view_kwargs)

        view_kwargs = self.view2_kwargs or {}
        return self.view2(request, **view_kwargs)


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
