"""Forms of the ``django_libs`` app."""
from django import forms


class PlaceholderForm(forms.Form):
    """Form to add the field's label as a placeholder attribute."""
    def __init__(self, *args, **kwargs):
        super(PlaceholderForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            if type(field.widget) in (forms.TextInput, forms.DateInput):
                field.widget = forms.TextInput(
                    attrs={'placeholder': field.label})
