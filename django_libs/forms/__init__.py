"""Forms of the ``django_libs`` app."""
from django.utils.html import strip_tags


class PlaceholderForm(object):
    """Form to add the field's label as a placeholder attribute."""
    def __init__(self, *args, **kwargs):
        super(PlaceholderForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[
                field_name].label


class StripTagsFormMixin(object):
    """
    Mixin that allows to strip html tags entered to some fields.

    Usage:

    1. In your form, inherit from this mixin
    2. In your form, add STRIP_TAGS_FIELDS = ['field_name1', 'field_name2', ]
       to the form class
    3. In your form's `__init__` call `self.strip_tags()` after your `super`
       call.

    """
    def strip_tags(self):
        form_data = self.data.copy()
        for field_name in self.STRIP_TAGS_FIELDS:
            if self.prefix:
                field_name = '{0}-{1}'.format(self.prefix, field_name)
            if field_name in form_data:
                field_data = form_data[field_name]
                field_data = strip_tags(field_data)
                form_data[field_name] = field_data
        self.data = form_data
