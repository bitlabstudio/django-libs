Template Tags
=============


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
with args and kwargs, just like you love to do it in Python and hate not to be
able to do it in Django templates.

Usage::

    {% load libs_tags %}
    {% call myobj 'mymethod' arg1 arg2 kwarg1=kwarg1 as result %}
    {{ result }}


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
    {% render_analytics_code False %}

If you would like to override the template used by the tag, please use
``django_libs/analytics.html``.


set_context
-----------

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
