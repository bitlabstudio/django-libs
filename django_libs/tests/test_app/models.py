"""Models for the ``test_app`` app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from simple_translation.translation_pool import translation_pool

from ...models_mixins import (
    SimpleTranslationMixin,
    SimpleTranslationPublishedManager,
)


class DummyProfile(SimpleTranslationMixin, models.Model):
    """Just a dummy profile model for testing purposes."""
    user = models.ForeignKey('auth.User')
    dummy_field = models.CharField(
        verbose_name=_('Dummy Field'),
        max_length=128,
    )

    objects = SimpleTranslationPublishedManager()


class DummyProfileTranslation(models.Model):
    """Just a translation of the dummy profile."""
    dummy_translation = models.CharField(max_length=128)

    is_published = models.BooleanField(default=True)
    language = models.CharField(max_length=8, default='en')

    dummyprofile = models.ForeignKey(DummyProfile)


translation_pool.register_translation(DummyProfile, DummyProfileTranslation)
