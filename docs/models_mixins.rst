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


SimpleTranslationPublishedManager
---------------------------------

When your model ``MyModel`` has a corresponding ``MyModelTranslation`` model,
like above, you can use the ``SimpleTranslationPublishedManager`` to filter for
published versions of ``MyModel``.

To set it up simply add the manager to your model::

    from django_libs.models_mixins import SimpleTranslationPublishedManager

    class MyModel(models.Model):

        # some fields

        objects = SimpleTranslationPublishedManager()


    class MyModelTranslation(models.Model):

        # these fields are required
        is_published = models.BooleanField()
        language = models.CharField(max_length=16)


If you want to alter the required fields, because your models differ from our
assumed structure or you want to build it into your own custom manager, you can
inherit the ``SimpleTranslationPublishedManager`` like so::

    from django_libs.models_mixins import SimpleTranslationPublishedManager

    class MyModelManager(SimpleTranslationPublishedManager)
        # set these values, if your translation model or the fields differ from
        # the defaults
        published_field = `mymodeltranslation__published_it_is`
        language_field = `mymodeltranslation__language_used`


and then add the new ``MyModelManager`` to ``MyModel`` like we did above.

Usage
+++++

When you set it up correctly, you can use the manager like so::

    MyModel.objects.published(request)


Note, that you need to pass a request instance, so the manager can fetch the
language.
