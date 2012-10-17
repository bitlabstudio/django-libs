Libs Template Tags
==================

get_verbose
-----------------

``get_verbose`` is a simple template tag to provide the verbose name of an object's specific field.

This can be useful when you are creating a ``DetailView`` for an object where, for some
reason you don't want to use a ModelForm. Instead of using the ``{% trans %}`` tag
to create your labels and headlines that are related to the object's fields, you can
now obey the DRY principle and re-use the translations that you have already done
on the model's field's ``verbose_name`` attributes.

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


navactive
-----------------

``navactive`` is a simple template tag to provide the string ``active`` if the current URL is in the desired url path.

In order to use it, just import the tag library and set the tag, e.g. as a css class::

    {% load libs_tags %}
    <ul class="nav">
        <li class="{% navactive request "/news/" exact=1 %}">
            <a href="{% url "news_list" %}">{% trans "News" %}</a>
        </li>
        <li class="{% navactive request "/news/" %}">
            <a href="{% url "news_detail" pk=latest.pk %}">{% trans "Latest News Entry" %}</a>
        </li>
    </ul>
