"""Custom form widgets."""
import django
from django.conf import settings
from django.forms import widgets, TextInput
from django.template import Context
from django.template.loader import get_template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

if django.VERSION >= (1, 7):
    from django.forms.utils import flatatt
else:
    from django.forms.util import flatatt


class LibsImageWidget(widgets.ClearableFileInput):
    """
    A better file input widget.

    Remember to include the js file as well. See docs for details.

    """

    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')
    clear_checkbox_label = ugettext_lazy('Clear')
    template_path = 'django_libs/partials/libs_image_widget.html'

    def __init__(self, attrs=None):
        if attrs:
            self.classes = attrs.get('class', '')
        else:
            self.classes = ''
        super(LibsImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        checkbox_name = self.clear_checkbox_name(name)
        checkbox_id = self.clear_checkbox_id(checkbox_name)
        context = {
            'checkbox_name': conditional_escape(checkbox_name),
            'checkbox_id': conditional_escape(checkbox_id),
            'checkbox_label': self.clear_checkbox_label,
            'input_id': '#{0}'.format(final_attrs['id']),
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'classes': self.classes,
            'widget': self,
            'value': value,
            'input': mark_safe('<input{0}/>'.format(flatatt(final_attrs))),
        }

        if value is None:
            value = ''
        if value and hasattr(value, "url"):
            # Only add the 'value' attribute if a value is non-empty.
            context.update({'initial': True})
            if value.url:
                context.update({
                    'src': value.url,
                    'file_name': value.url.split('/')[-1]})
                if not self.is_required:
                    context.update({
                        'clear_widget': widgets.CheckboxInput().render(
                            checkbox_name, False, attrs={'id': checkbox_id})})

        t = get_template(self.template_path)
        c = Context(context)
        return t.render(c)


class ColorPickerWidget(TextInput):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'django_libs/css/colorpicker.css',
            )
        }
        js = (
            settings.STATIC_URL + 'django_libs/js/jquery-1.11.1.min.js',
            settings.STATIC_URL + 'django_libs/js/colorpicker.js',
            settings.STATIC_URL + 'django_libs/js/colorpicker_list.js',
            settings.STATIC_URL + 'django_libs/js/eye.js',
            settings.STATIC_URL + 'django_libs/js/layout.js',
            settings.STATIC_URL + 'django_libs/js/utils.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(ColorPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(ColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(
            u'''<script type="text/javascript">
                $('#id_%s').ColorPicker({
                onSubmit: function(hsb, hex, rgb, el) {
                    $(el).val(hex);
                    $(el).ColorPickerHide();
                },
                onBeforeShow: function () {
                    $(this).ColorPickerSetColor(this.value);
                }
             }).bind('keyup', function(){
                 $(this).ColorPickerSetColor(this.value);
             });
            </script>''' % name)
