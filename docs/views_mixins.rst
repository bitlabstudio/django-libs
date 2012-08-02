Views Mixins
===========

JSONResponseMixin
-----------------

You can find out more about the ``JSONResponseMixin`` in the official Django
docs: https://docs.djangoproject.com/en/dev/topics/class-based-views/#more-than-just-html

In order to use it, just import is like all the other generic class based views
and view mixins::

    from django.views.generic import View
    from django_libs.views_mixins import JSONResponseMixin

    class MyAPIView(JSONResponseMixin, View):
        pass
