Models Mixins
=============

TranslationModelMixin
---------------------

hvad's ``safe_translation_getter`` doesn't care about untranslated objects, so
we built this mixin to add some falllbacks

You can use this by inheriting the class::

    from django.db import models

    from hvad.models import TranslatableModel, TranslatedFields
    from django_libs.models_mixins import TranslationModelMixin


    class HvadModel(TranslationModelMixin, TranslatableModel):
        translations = TranslatedFields(
            title=models.CharField(
                verbose_name=_('Title'),
                max_length=256,
            ),
        )

This mixin will automatically return the title field if its ``__unicode__``
function is called and it will always return a title string (no pk fallback or
anything like that needed). If there's no translation available in the current
language it searches for others.
