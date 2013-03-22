"""Models for the ``test_app`` app."""
from django.db import models


class DummyProfile(models.Model):
    """Just a dummy profile model for testing purposes."""
    user = models.ForeignKey('auth.User')
    dummy_field = models.CharField(max_length=128)
