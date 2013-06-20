"""Templatetags for the ``django_libs`` project."""
import importlib

from django import template
from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404
from django.db.models.fields import FieldDoesNotExist

from django_libs import utils


register = template.Library()


@register.assignment_tag
def call(obj, method, *args, **kwargs):
    """
    Allows to call any method of any object with parameters.

    Because come on! It's bloody stupid that Django's templating engine doesn't
    allow that.

    Usage::

        {% call myobj 'mymethod' myvar foobar=myvar2 as result %}

    :param obj: The object which has the method that you would like to call
    :param method: A string representing the attribute on the object that
      should be called.

    """
    return getattr(obj, method)(*args, **kwargs)


@register.filter
def get_verbose(obj, field_name=""):
    """
    Returns the verbose name of an object's field.

    :param obj: A model instance.
    :param field_name: The requested field value in string format.

    """
    if hasattr(obj, "_meta") and hasattr(obj._meta, "get_field_by_name"):
        try:
            return obj._meta.get_field_by_name(field_name)[0].verbose_name
        except FieldDoesNotExist:
            pass
    return ""


@register.assignment_tag
def get_profile_for(user):
    return utils.get_profile(user)


class LoadContextNode(template.Node):
    def __init__(self, fqn):
        self.fqn = fqn

    def render(self, context):
        module = importlib.import_module(self.fqn)
        for attr in dir(module):
            if not attr.startswith('__'):
                context[attr] = getattr(module, attr)
        return ''


@register.tag
def load_context(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, fqn = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires a single argument' % token.contents.split()[0])
    if not (fqn[0] == fqn[-1] and fqn[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)
    return LoadContextNode(fqn[1:-1])


@register.simple_tag
def navactive(request, url, exact=0):
    """
    Returns ``active`` if the given URL is in the url path, otherwise ''.

    Usage::

        {% load libs_tags %}
        ...
        <li class="{% navactive request "/news/" exact=1 %}">

    :param request: A request instance.
    :param url: A string representing a part of the URL that needs to exist
      in order for this method to return ``True``.
    :param exact: If ``1`` then the parameter ``url`` must be equal to
      ``request.path``, otherwise the parameter ``url`` can just be a part of
      ``request.path``.

    """
    try:
        if url == resolve(request.path).url_name:
            # Checks the url pattern in case a view_name is posted
            return 'active'
        elif url == request.path:
            # Workaround to catch URLs with more than one part, which don't
            # raise a Resolver404 (e.g. '/index/info/')
            match = request.path
        else:
            return ''
    except Resolver404:
        # Indicates, that a simple url string is used (e.g. '/index/')
        match = request.path
    if exact and url == match:
        return 'active'
    elif not exact and url in request.path:
        return 'active'
    return ''


@register.inclusion_tag('django_libs/analytics.html')
def render_analytics_code(anonymize_ip='anonymize'):
    """
    Renders the google analytics snippet.

    :anonymize_ip: Use to add/refuse the anonymizeIp setting.

    """
    return {
        'ANALYTICS_TRACKING_ID': getattr(
            settings, 'ANALYTICS_TRACKING_ID', 'UA-XXXXXXX-XX'),
        'anonymize_ip': anonymize_ip,
    }
