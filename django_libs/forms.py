"""Forms of the ``django_libs`` app."""
class PlaceholderForm(object):
    """Form to add the field's label as a placeholder attribute."""
    def __init__(self, *args, **kwargs):
        super(PlaceholderForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[
                field_name].label
