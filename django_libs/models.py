"""Models of the ``django_libs`` projects."""
from django.core.validators import RegexValidator
from django.db.models import CharField

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ["^django_libs\.models\.ColorField"])

from .widgets import ColorPickerWidget


class ColorField(CharField):
    """Custom color field to display a color picker."""
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super(ColorField, self).__init__(*args, **kwargs)
        self.validators.append(RegexValidator(
            regex='^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
            message='Only RGB color model inputs allowed, like FF00CC',
            code='nomatch'))

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super(ColorField, self).formfield(**kwargs)
