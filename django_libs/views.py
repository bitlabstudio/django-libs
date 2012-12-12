"""Views for testing 404 and 500 templates."""
from django.views.generic import TemplateView


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
