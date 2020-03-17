"""Templatetags for the ``django_libs`` project."""
import datetime
import importlib

from django import template
try:
    from django.template.base import TOKEN_BLOCK, TOKEN_VAR
except ImportError:
    from django.template.base import TokenType
    TOKEN_BLOCK = TokenType.BLOCK
    TOKEN_VAR = TokenType.VAR
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db.models.fields import FieldDoesNotExist
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text

try:  # django <= 1.6
    from django.core.urlresolvers import resolve, Resolver404
except ImportError:  # >= django 1.7
    from django.urls import resolve, Resolver404

from ..loaders import load_member

register = template.Library()
register_tag = register.assignment_tag if hasattr(
    register, 'assignment_tag') else register.simple_tag


@register_tag
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

        {% add_form_widget_attr field 'class' 'form-control' replace=1 as
          field_ %}


    """
    if not replace:
        attr = field.field.widget.attrs.get(attr_name, '')
        attr += force_text(attr_value)
        field.field.widget.attrs[attr_name] = attr
        return field
    else:
        field.field.widget.attrs[attr_name] = attr_value
        return field


@register.tag('block_anyfilter')
def block_anyfilter(parser, token):
    """
    Turn any template filter into a blocktag.

    Usage::

    {% load libs_tags %}
    {% block_anyfilter django.template.defaultfilters.truncatewords_html 15 %}
        // Something complex that generates html output
    {% endblockanyfilter %}

    """
    bits = token.contents.split()
    nodelist = parser.parse(('endblockanyfilter',))
    parser.delete_first_token()
    return BlockAnyFilterNode(nodelist, bits[1], *bits[2:])


class BlockAnyFilterNode(template.Node):

    def __init__(self, nodelist, original_tag_fqn, *args):
        self.nodelist = nodelist
        self.original_tag = load_member(original_tag_fqn)
        self.args = args

    def render(self, context):
        output = self.nodelist.render(context)
        return self.original_tag(output, *self.args)


@register_tag
def calculate_dimensions(image, long_side, short_side):
    """Returns the thumbnail dimensions depending on the images format."""
    if image.width >= image.height:
        return '{0}x{1}'.format(long_side, short_side)
    return '{0}x{1}'.format(short_side, long_side)


@register_tag
def call(obj, method, *args, **kwargs):
    """
    Allows to call any method of any object with parameters.

    Because come on! It's bloody stupid that Django's templating engine doesn't
    allow that.

    Usage::

        {% call myobj 'mymethod' myvar foobar=myvar2 as result %}
        {% call myobj 'mydict' 'mykey' as result %}
        {% call myobj 'myattribute' as result %}

    :param obj: The object which has the method that you would like to call
    :param method: A string representing the attribute on the object that
      should be called.

    """
    function_or_dict_or_member = getattr(obj, method)
    if callable(function_or_dict_or_member):
        # If it is a function, let's call it
        return function_or_dict_or_member(*args, **kwargs)
    if not len(args):
        # If it is a member, lets return it
        return function_or_dict_or_member
    # If it is a dict, let's access one of it's keys
    return function_or_dict_or_member[args[0]]


@register_tag
def concatenate(*args, **kwargs):
    """
    Concatenates the given strings.

    Usage::

        {% load libs_tags %}
        {% concatenate "foo" "bar" as new_string %}
        {% concatenate "foo" "bar" divider="_" as another_string %}

    The above would result in the strings "foobar" and "foo_bar".

    """
    divider = kwargs.get('divider', '')
    result = ''
    for arg in args:
        if result == '':
            result += arg
        else:
            result += '{0}{1}'.format(divider, arg)
    return result


@register.filter
def get_content_type(obj, field_name=False):
    """
    Returns the content type of an object.

    :param obj: A model instance.
    :param field_name: Field of the object to return.

    """
    content_type = ContentType.objects.get_for_model(obj)
    if field_name:
        return getattr(content_type, field_name, '')
    return content_type


@register_tag
def get_form_field_type(field):
    """
    Returns the widget type of the given form field.

    This can be helpful if you want to render form fields in your own way
    (i.e. following Bootstrap standards).

    Usage::

        {% load libs_tags %}
        {% for field in form %}
            {% get_form_field_type field as field_type %}
            {% if "CheckboxInput" in field_type %}
                <div class="checkbox">
                    <label>
                        // render input here
                    </label>
                </div>
            {% else %}
                {{ field }}
            {% endif %}
        {% endfor %}

    """
    return field.field.widget.__str__()


@register.filter
def get_verbose(obj, field_name=""):
    """
    Returns the verbose name of an object's field.

    :param obj: A model instance.
    :param field_name: The requested field value in string format.

    """
    if hasattr(obj, "_meta") and hasattr(obj._meta, "get_field_by_name"):
        try:
            return obj._meta.get_field(field_name).verbose_name
        except FieldDoesNotExist:
            pass
    return ""


@register_tag
def get_query_params(request, *args):
    """
    Allows to change one of the URL get parameter while keeping all the others.

    Usage::

      {% load libs_tags %}
      {% get_query_params request "page" page_obj.next_page_number as query %}
      <a href="?{{ query }}">Next</a>

    You can also pass in several pairs of keys and values::

      {% get_query_params request "page" 1 "foobar" 2 as query %}

    You often need this when you have a paginated set of objects with filters.

    Your url would look something like ``/?region=1&gender=m``. Your paginator
    needs to create links with ``&page=2`` in them but you must keep the
    filter values when switching pages.

    :param request: The request instance.
    :param *args: Make sure to always pass in paris of args. One is the key,
      one is the value. If you set the value of a key to "!remove" that
      parameter will not be included in the returned query.

    """
    query = request.GET.copy()
    index = 1
    key = ''
    for arg in args:
        if index % 2 != 0:
            key = arg
        else:
            if arg == "!remove":
                try:
                    query.pop(key)
                except KeyError:
                    pass
            else:
                query[key] = arg
        index += 1
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
    if not hasattr(request, 'path'):
        return ''
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
    else:
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


@register_tag
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
        {% get_range_around page_obj.paginator.num_pages page_obj.number 5
          as pages %}

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
        range_items = range(1, range_value + 1)
        return {
            'range_items': range_items,
            'left_padding': False,
            'right_padding': False,
        }
    if current_item <= left_bound:
        range_items = range(1, range_value + 1)[:total_items]
        return {
            'range_items': range_items,
            'left_padding': range_items[0] > 1,
            'right_padding': range_items[-1] < range_value,
        }

    if current_item >= right_bound:
        range_items = range(1, range_value + 1)[-total_items:]
        return {
            'range_items': range_items,
            'left_padding': range_items[0] > 1,
            'right_padding': range_items[-1] < range_value,
        }

    range_items = range(current_item - padding, current_item + padding + 1)
    return {
        'range_items': range_items,
        'left_padding': True,
        'right_padding': True,
    }


@register_tag(takes_context=True)
def is_context_variable(context, variable_name):
    """
    Returns true if the given variable name is in the template context.

    Usage::

        {% is_context_variable "variable_name" as variable_exists %}
        {% if variable_exists %}
            ...
        {% endif %}

    """
    return variable_name in context


@register.inclusion_tag('django_libs/analytics.html')
def render_analytics_code():
    """
    Renders the new google analytics snippet.

    """
    return {
        'ANALYTICS_TRACKING_ID': getattr(settings, 'ANALYTICS_TRACKING_ID',
                                         'UA-XXXXXXX-XX'),
        'ANALYTICS_DOMAIN': getattr(settings, 'ANALYTICS_DOMAIN', 'auto')
    }


@register.simple_tag(takes_context=True)
def save(context, key, value):
    """
    Saves any value to the template context.

    Usage::

        {% save "MYVAR" 42 %}
        {{ MYVAR }}

    """
    context.dicts[0][key] = value
    return ''


@register.simple_tag(takes_context=True)
def sum(context, key, value, multiplier=1):
    """
    Adds the given value to the total value currently held in ``key``.

    Use the multiplier if you want to turn a positive value into a negative
    and actually substract from the current total sum.

    Usage::

        {% sum "MY_TOTAL" 42 -1 %}
        {{ MY_TOTAL }}

    """
    if key not in context.dicts[0]:
        context.dicts[0][key] = 0
    context.dicts[0][key] += value * multiplier
    return ''


@register_tag
def set_context(value):
    return value


class VerbatimNode(template.Node):

    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


@register.tag
def verbatim(parser, token):
    """Tag to render x-tmpl templates with Django template code."""
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == TOKEN_VAR:
            text.append('{{ ')
        elif token.token_type == TOKEN_BLOCK:
            text.append('{%')
        text.append(token.contents)
        if token.token_type == TOKEN_VAR:
            text.append(' }}')
        elif token.token_type == TOKEN_BLOCK:
            if not text[-1].startswith('='):
                text[-1:-1] = [' ']
            text.append(' %}')
    return VerbatimNode(''.join(text))


@register.filter
def exclude(qs, qs_to_exclude):
    """Tag to exclude a qs from another."""
    return qs.exclude(pk__in=qs_to_exclude.values_list('pk'))


@register_tag
def time_until(date_or_datetime):
    if isinstance(date_or_datetime, datetime.date):
        datetime_ = datetime.datetime(date_or_datetime.year,
                                      date_or_datetime.month,
                                      date_or_datetime.day, 0, 0)
    else:
        datetime_ = date_or_datetime
    return datetime_ - datetime.datetime.now()


@register_tag
def days_until(date_or_datetime):
    days = time_until(date_or_datetime).days
    if days >= 0:
        return days
    return 0


@register_tag
def hours_until(date_or_datetime):
    closes_in = time_until(date_or_datetime)
    if closes_in.days < 0:
        return 0
    return closes_in.seconds / 3600


@register_tag
def minutes_until(date_or_datetime):
    closes_in = time_until(date_or_datetime)
    if closes_in.days < 0:
        return 0
    return closes_in.seconds / 60 - hours_until(date_or_datetime) * 60


@register.filter(is_safe=False)
@stringfilter
def append_s(value):
    """
    Adds the possessive s after a string.

    value = 'Hans' becomes Hans'
    and value = 'Susi' becomes Susi's

    """
    if value.endswith('s'):
        return u"{0}'".format(value)
    else:
        return u"{0}'s".format(value)


@register_tag
def get_site():
    return Site.objects.get_current()
