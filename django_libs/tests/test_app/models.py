"""Models for the ``test_app`` app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hvad.models import TranslatableModel, TranslatedFields

from ...models_mixins import TranslationModelMixin


class HvadDummy(TranslationModelMixin, TranslatableModel):
    """Dummy model to test hvad stuff."""
    translations = TranslatedFields(
        title=models.CharField(
            verbose_name=_('Title'),
            max_length=256,
        ),
    )


class DummyProfile(models.Model):
    """Just a dummy profile model for testing purposes."""
    user = models.ForeignKey('auth.User')
    dummy_field = models.CharField(
        verbose_name=_('Dummy Field'),
        max_length=128,
    )
