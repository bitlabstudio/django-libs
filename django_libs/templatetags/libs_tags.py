"""Templatetags for the ``django_libs`` project."""
from django import template
from django.db.models.fields import FieldDoesNotExist

register = template.Library()


@register.filter
def get_verbose(obj, field_name=""):
    """
    Returns the verbose name of an object's field.

    """
    if hasattr(obj, "_meta") and hasattr(obj._meta, "get_field_by_name"):
        try:
            return obj._meta.get_field_by_name(field_name)[0].verbose_name
        except FieldDoesNotExist:
            pass
    return ""
