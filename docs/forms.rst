Forms
=====

PlaceholderForm
---------------

Simple form mixin, which uses the field label as a placeholder attribute. E.g.:

    first_name = forms.CharField(label=_('Name'))

will be rendered as:

    <input id="id_first_name" name="first_name" placeholder="Name" type="text">


StripTagsFormMixin
------------------

A mixin that allows to mark certain fields to not allow any HTML tags.

Then the form gets initiated and data is given, all HTML tags will be stripped
away from that data.

Usage::

    class MyForm(StripTagsFormMixin, forms.Form):
        text = forms.CharField(max_length=1000)

        STRIP_TAGS_FIELDS = ['text', ]

        def __init__(self, *args, **kwargs):
            super(MyForm, self).__init__(*args, **kwargs)
            self.strip_tags()

1. Inherit from `StripTagsFormMixin`
2. Add `STRIP_TAGS_FIELDS` attribute to your form class
3. Override `__init__` and call `self.strip_tags()` after your super call
