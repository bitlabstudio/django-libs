"""Templatetags for the ``django_libs`` project."""
import importlib

from django import template
from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404
from django.db.models.fields import FieldDoesNotExist
from django.template.defaultfilters import truncatewords_html

from django_libs import utils


register = template.Library()


@register.assignment_tag
def add_form_widget_attr(field, attr_name, attr_value, replace=0):
    """
    Adds widget attributes to a bound form field.

    This is helpful if you would like to add a certain class to all your forms
    (i.e. `form-control` to all form fields when you are using Bootstrap)::

        {% load libs_tags %}
        {% for field in form.fields %}
            {% add_form_widget_attr field 'class' 'form-control' as field_ %}
            {{ field_ }}
        {% endfor %}

    The tag will check if the attr already exists and only append your value.
    If you would like to replace existing attrs, set `replace=1`::

        {% add_form_widget_attr field 'class' 'form-control' replace=1 as field_ %}


    """
    if not replace:
        attr = field.field.widget.attrs.get(attr_name, '')
        attr += attr_value
        field.field.widget.attrs[attr_name] = attr
        return field
    else:
        field.field.widget.attrs[attr_name] = attr_value
        return field


@register.tag('block_truncatewords_html')
def block_truncatewords_html(parser, token):
    """
    Allows to truncate any block of content.

    This is useful when rendering other tags that generate content,
    such as django-cms' ``render_placeholder`` tag, which is not available
    as an assignment tag::

        {% load libs_tags %}
        {% block_truncatewords_html 15 %}
            {% render_placeholder object.placeholder %}
        {% endblocktruncatewordshtml %}

    """
    bits = token.contents.split()
    try:
        word_count = bits[1]
    except IndexError:
        word_count = 15
    nodelist = parser.parse(('endblocktruncatewordshtml',))
    parser.delete_first_token()
    return BlockTruncateWordsHtmlNode(nodelist, word_count)


class BlockTruncateWordsHtmlNode(template.Node):
    def __init__(self, nodelist, word_count):
        self.nodelist = nodelist
        self.word_count = word_count

    def render(self, context):
        output = self.nodelist.render(context)
        return truncatewords_html(output, self.word_count)


@register.assignment_tag
def calculate_dimensions(image, long_side, short_side):
    """Returns the thumbnail dimensions depending on the images format."""
    if image.width >= image.height:
        return '{0}x{1}'.format(long_side, short_side)
    return '{0}x{1}'.format(short_side, long_side)


@register.assignment_tag
def call(obj, method, *args, **kwargs):
    """
    Allows to call any method of any object with parameters.

    Because come on! It's bloody stupid that Django's templating engine doesn't
    allow that.

    Usage::

        {% call myobj 'mymethod' myvar foobar=myvar2 as result %}

    :param obj: The object which has the method that you would like to call
    :param method: A string representing the attribute on the object that
      should be called.

    """
    return getattr(obj, method)(*args, **kwargs)


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


@register.assignment_tag
def get_profile_for(user):
    """
    Allows to call the get_profile utility function from django-libs in a
    template.

    """
    return utils.get_profile(user)


@register.assignment_tag
def get_query_params(request, param_name, param_value):
    """
    Allows to change one of the URL get parameter while keeping all the others.

    Usage::

      {% load libs_tags %}
      {% get_query_params request "page" page_obj.next_page_number as query %}
      <a href="?{{ query }}">Next</a>

    You often need this when you have a paginated set of objects with filters.

    Your url would look something like ``/?region=1&gender=m``. Your paginator
    needs to create links with ``&page=2`` in them but you must keep the
    filter values when switching pages.

    :param request: The request instance.
    :param param_name: The name of the parameter that should be added or
      updated.
    :param param_value: The value of the parameter that should be added or
      updated.

    """
    query = request.GET.copy()
    query[param_name] = param_value
    return query.urlencode()


class LoadContextNode(template.Node):
    def __init__(self, fqn):
        self.fqn = fqn

    def render(self, context):
        module = importlib.import_module(self.fqn)
        for attr in dir(module):
            if not attr.startswith('__'):
                context[attr] = getattr(module, attr)
        return ''


@register.tag
def load_context(parser, token):
    # TODO Docstring!
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, fqn = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires a single argument' % token.contents.split()[0])
    if not (fqn[0] == fqn[-1] and fqn[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)
    return LoadContextNode(fqn[1:-1])


@register.simple_tag
def navactive(request, url, exact=0, use_resolver=1):
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
    :use_resolver: If ``0`` we will not try to compare ``url`` with existing
      view names but we will only compare it with ``request.path``.

    """
    if use_resolver:
        try:
            if url == resolve(request.path).url_name:
                # Checks the url pattern in case a view_name is posted
                return 'active'
            elif url == request.path:
                # Workaround to catch URLs with more than one part, which don't
                # raise a Resolver404 (e.g. '/index/info/')
                match = request.path
            else:
                return ''
        except Resolver404:
            # Indicates, that a simple url string is used (e.g. '/index/')
            match = request.path

    if exact and url == match:
        return 'active'
    elif not exact and url in request.path:
        return 'active'
    return ''


@register.filter
def get_range(value, max_num=None):
    """
    Returns the range over a given value.

    Usage::

        {% load libs_tags %}

        {% for item in object_list.count|get_range %}
            {{ item }} // render real items here
        {% endfor %}
        {% for item in object_list.count|get_range:5 %}
            // render placeholder items here
        {% endfor %}

    :param value: The number to pass to the range function
    :param max_num: Optional. Use this if you want to get a range over the
      difference between the actual number and a maximum amount. This can
      be useful to display placeholder items in a situation where the
      space must always be filled up with 5 items but your actual list
      might only have 2 items.

    """
    if max_num:
        value = max_num - value
    return range(value)


@register.assignment_tag
def get_range_around(range_value, current_item, padding):
    """
    Returns a range of numbers around the given number.

    This is useful for pagination, where you might want to show something
    like this::

        << < ... 4 5 (6) 7 8 .. > >>

    In this example `6` would be the current page and we show 2 items around
    that page (including the page itself).

    Usage::

        {% load libs_tags %}
        {% get_range_around page_obj.paginator.num_pages page_obj.number 5 as pages %}

    :param range_amount: Number of total items in your range (1 indexed)
    :param current_item: The item around which the result should be centered
      (1 indexed)
    :param padding: Number of items to show left and right from the current
      item.

    """
    total_items = 1 + padding * 2
    left_bound = padding
    right_bound = range_value - padding
    if range_value <= total_items:
        range_items = range(1, range_value+1)
        return {
            'range_items': range_items,
            'left_padding': False,
            'right_padding': False,
        }
    if current_item <= left_bound:
        range_items = range(current_item, range_value+1)[:total_items]
        return {
            'range_items': range_items,
            'left_padding': range_items[0] > 1,
            'right_padding': range_items[-1] < range_value,
        }

    if current_item >= right_bound:
        range_items = range(1, current_item+1)[-total_items:]
        return {
            'range_items': range_items,
            'left_padding': range_items[0] > 1,
            'right_padding': range_items[-1] < range_value,
        }

    range_items = range(current_item-padding, current_item+padding+1)
    return {
        'range_items': range_items,
        'left_padding': True,
        'right_padding': True,
    }


@register.inclusion_tag('django_libs/analytics.html')
def render_analytics_code(anonymize_ip='anonymize'):
    """
    Renders the google analytics snippet.

    :anonymize_ip: Use to add/refuse the anonymizeIp setting.

    """
    return {
        'ANALYTICS_TRACKING_ID': getattr(
            settings, 'ANALYTICS_TRACKING_ID', 'UA-XXXXXXX-XX'),
        'anonymize_ip': anonymize_ip,
    }


@register.inclusion_tag('django_libs/analytics2.html')
def render_analytics2_code():
    """
    Renders the new google analytics snippet.

    """
    return {
        'ANALYTICS_TRACKING_ID': getattr(
            settings, 'ANALYTICS_TRACKING_ID', 'UA-XXXXXXX-XX'),
        'ANALYTICS_DOMAIN': getattr(
            settings, 'ANALYTICS_DOMAIN', 'example.com')
    }


class VerbatimNode(template.Node):
    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


@register.assignment_tag
def set_context(value):
    return value


@register.tag
def verbatim(parser, token):
    """Tag to render x-tmpl templates with Django template code."""
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{ ')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{%')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append(' }}')
        elif token.token_type == template.TOKEN_BLOCK:
            if not text[-1].startswith('='):
                text[-1:-1] = [' ']
            text.append(' %}')
    return VerbatimNode(''.join(text))
