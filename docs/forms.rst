Forms
=====

PlaceholderForm
---------------

Simple form mixin, which uses the field label as a placeholder attribute. E.g.:

    first_name = forms.CharField(label=_('Name'))

will be rendered as:

    <input id="id_first_name" name="first_name" placeholder="Name" type="text">
