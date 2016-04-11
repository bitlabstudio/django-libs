Fields
======

ColorField
----------

If you want to store hex color code to a field, you can make use of the
``ColorField``. It also provides a color picker, which can be used in the
admin.

Simple add it to your color classes::

    from django.db import models

    from hvad.models import TranslatableModel, TranslatedFields
    from django_libs.models_mixins import TranslationModelMixin


    class Category(models.Model):
        color = ColorField()
