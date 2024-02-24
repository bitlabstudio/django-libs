from django import template

register = template.Library()


@register.filter
def upper(text):
    return text.upper()
