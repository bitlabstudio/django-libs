Models Mixins
=============

SimpleTranslationMixin
----------------------

We ended up adding a ``get_translation`` method to all models that have a
corresponding translation model, so this mixin will add common methods needed
by models under
`simple-translation <https://github.com/fivethreeo/simple-translation>`_.

You can use this by inheriting the class::

    from django.db import models
    from django_libs.models_mixins import SimpleTranslationMixin

    class MyModel(SimpleTranslationMixin, models.Model):
        pass

    class MyModelTranslation(models.Model):
        name = models.CharField(max_length=256)

        # needed by simple-translation
        my_model = models.ForeignKey(MyModel)
        language = models.CharField(max_length=16)


get_translation
+++++++++++++++

The method takes an optional parameter ``language`` if you want to get a
specific translation, otherwise it will return the translation for the
currently active language::

    myobject = MyModel.objects.get(pk=1)
    trans = myobject.get_translation()
    print trans.name
