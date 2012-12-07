"""Views for testing 404 and 500 templates."""
from django.views.generic import TemplateView


class Http404TestView(TemplateView):
    template_name = '404.html'


class Http500TestView(TemplateView):
    template_name = '500.html'
