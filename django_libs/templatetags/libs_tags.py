"""Templatetags for the ``django_libs`` project."""
from django import template
from django.db.models.fields import FieldDoesNotExist

register = template.Library()


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
    if exact:
        if url == request.path:
            return "active"
        return ""

    if url in request.path:
        return "active"
    return ""
