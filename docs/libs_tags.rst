Template Tags
=============

add_form_widget_attr
--------------------
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


block_truncatewords_html
------------------------
Allows to truncate any block of content. Calls Django's ``truncatewords_html``
internally.

This is useful when rendering other tags that generate content,
such as django-cms' ``render_placeholder`` tag, which is not available
as an assignment tag::

    {% load libs_tags %}
    {% block_truncatewords_html 15 %}
        {% render_placeholder object.placeholder %}
    {% endblocktruncatewordshtml %}

The first parameter is the number of words you would like to truncate after.


calculate_dimensions
--------------------

``calculate_dimensions`` is a way to auto-correct thumbnail dimensions
depending on the images format. The required args are am image instance, the
length of the long image side and finally the length of the short image side.

Usage Example with easy_thumbnails::

    {% load libs_tags thumbnail %}
    {% calculate_dimensions image 320 240 as dimensions%}
    <img src="{% thumbnail image dimensions %}" />


It then ouputs ``320x240`` if the image is landscape and ``240x320`` if the
image is portait.



call
----

``call`` is an assignemnt tag that allows you to call any method of any object
with args and kwargs, because you do it in Python all the time and you hate not
to be able to do it in Django templates.

Usage::

    {% load libs_tags %}
    {% call myobj 'mymethod' myvar foobar=myvar2 as result %}
    {% call myobj 'mydict' 'mykey' as result %}
    {% call myobj 'myattribute' as result %}
    {{ result }}


concatenate
-----------

Concatenates the given strings.

Usage::

    {% load libs_tags %}
    {% concatenate "foo" "bar" as new_string %}
    {% concatenate "foo" "bar" divider="_" as another_string %}

The above would result in the strings "foobar" and "foo_bar".


exclude
-------

``exclude`` is a filter tag that allows you to exclude one queryset from
another.

Usage::

    {% load libs_tags %}
    {% for clean_obj in qs|exclude:dirty_qs %}
        {{ clean_obj }}
    {% endfor %}


get_form_field_type
-------------------
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


get_range
---------

``get_range`` behaves just like Python's ``range`` function and allows you to
iterate over ranges in your templates::

    {% load libs_tags %}
    {% for item in 5|get_range %}
        Item number {{ item }}
    {% endfor %}

You can also calculate the difference between your value and a max value.
This is useful if you want to fill up empty space with items so that the
total amount of items is always ``max_num``::

    {% load libs_tags %}
    {% for item in object_list.count|get_range %}
        // render the actual items
    {% endfor %}
    {% for item in object_list.count|get_range:10 %}
        // render the placeholder items to fill up the space
    {% endfor %}

get_range_around
----------------
Returns a range of numbers around the given number.

This is useful for pagination, where you might want to show something
like this::

    << < ... 4 5 (6) 7 8 .. > >>

In this example `6` would be the current page and we show 2 items left and
right of that page.

Usage::

    {% load libs_tags %}
    {% get_range_around page_obj.paginator.num_pages page_obj.number 2 as pages %}

The parameters are:

1. range_amount: Number of total items in your range (1 indexed)
2. The item around which the result should be centered (1 indexed)
3. Number of items to show left and right from the current item.


get_verbose
-----------

``get_verbose`` is a simple template tag to provide the verbose name of an
object's specific field.

This can be useful when you are creating a ``DetailView`` for an object where,
for some reason you don't want to use a ModelForm. Instead of using the
``{% trans %}`` tag to create your labels and headlines that are related to
the object's fields, you can now obey the DRY principle and re-use the
translations that you have already done on the model's field's
``verbose_name`` attributes.

In order to use it, just import the tag library and set the tag::

    {% load libs_tags %}
    <ul>
        <li>
            <span>{{ news|get_verbose:"date" }}</span>
        </li>
        <li>
            <span>{{ news|get_verbose:"title" }}</span>
        </li>
    </ul>


get_query_params
----------------

Allows to change (or add) one of the URL get parameter while keeping all the
others.

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


load_context
------------

``load_context`` allows you to load any python module and add all it's
attributes to the current template's context. This is very useful for the
RapidPrototypingView, for example. You would be able to create the template
without having any view providing a useful context (because the view might
not exist, yet). But as a template designer you might already know that the
view will definitely return a list of objects and that list will be called
``objects`` and each object will have a ``name`` attribute.

Here is how you would use it:

* create a file ``yourproject/context/__init__.py``
* create a file ``yourproject/context/home.py``. A good convention would be
  to name these context modules just like you would name your templates.

Now create the context that you would like to use in your ``home.html``
template::

    # in object_list.py:
    objects = [
        {'name': 'Object 1', },
        {'name': 'Object 2', },
    ]

Now create your template::

    # in home.html
    {% load libs_tags %}
    {% load_context "myproject.context.home" %}

    {% for object in objects %}
        <h1>{{ object.name }}</h1>
    {% endfor %}

This should allow your designers to create templates long before the developers
have finished the views.


navactive
---------

``navactive`` is a simple template tag to provide the string ``active`` if
the current URL is in the desired url path.

In order to use it, just import the tag library and set the tag, e.g. as a
css class::

    {% load libs_tags %}
    <ul class="nav">
        <li class="{% navactive request "/news/" exact=1 %}">
            <a href="{% url "news_list" %}">{% trans "News" %}</a>
        </li>
        <li class="{% navactive request "/news/" %}">
            <a href="{% url "news_detail" pk=latest.pk %}">{% trans "Latest News Entry" %}</a>
        </li>
    </ul>


render_analytics_code
---------------------

``render_analytics_code`` is an inclusion tag to render Google's analytics
script code.

Usage::

    {% load libs_tags %}
    {% render_analytics_code %}


or (if you don't want to use the ``anonymizeIp`` setting)::

    {% load libs_tags %}
    ...
    <head>
    ...
    {% render_analytics_code False %}
    </head>

If you would like to override the template used by the tag, please use
``django_libs/analytics.html``.


render_analytics2_code
----------------------

The same as ``render_analytics_code`` but uses the new syntax and always uses
anonymize IP.

Usage::

    {% load libs_tags %}
    ...
    <head>
    ...
    {% render_analytics2_code %}
    </head>


save
----

``save`` allows you to save any variable to the context. This can be useful
when you have a template where different sections are rendered
depending on complex conditions. If you want to render `<hr />` tags between
those sections, it can be quite difficult to figure out when to render the
divider and when not.

Usage::

    {% load libs_tags %}
    ...
    {% if complex_condition1 %}
        // Render block 1
        {% save "NEEDS_HR" 1 %}
    {% endif %}

    {% if complex_condition2 %}
        {% if NEEDS_HR %}
            <hr />
            {% save "NEEDS_HR" 0 %}
        {% endif %}
        // Render block 2
        {% save "NEEDS_HR" 1 %}
    {% endif %}

When you have to render lots of divicers, the above example can become more
elegant when you replace the `if NEEDS_HR` block with::

    {% include "django_libs/partials/dynamic_hr.html" %}


set_context
-----------

NOTE: It turns out that this implementation only saves to the current
template's context. If you use this in a sub-template, it will not be available
in the parent template. Use our ``save`` tag for manipulating the global
RequestContext.

``set_context`` allows you to put any variable into the context. This can be
useful when you are creating prototype templates where you don't have the full
template context, yet but you already know that certain variables will be
available later::

    {% load libs_tags %}
    {% set_context '/dummy-url/' as contact_url %}
    {% blocktrans with contact_url=contact_url %}
    Please don't hesitate to <a href="{{ contact_url }}">contact us</a>.
    {% endblocktrans %}


verbatim
--------

``verbatim`` is a tag to render x-tmpl templates in Django templates without
losing the code structure.

Usage::

    {% load libs_tags %}
    {% verbatim %}
    {% if test1 %}
        {% test1 %}
    {% endif %}
    {{ test2 }}
    {% endverbatim %}


The output will be::

    {% if test1 %}
        {% test1 %}
    {% endif %}
    {{ test2 }}
