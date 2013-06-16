"""Additional helpful utility functions."""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .loaders import load_member_from_setting


def get_profile(user):
    """
    Makes sure to always return a valid profile for the user.

    If none exists, it creates one.

    :user: A Django ``User`` instance.

    """
    # try if we get a profile via the regular method
    try:
        return user.get_profile()
    except ObjectDoesNotExist:
        pass

    # check if we set a custom method for profile fetching
    setting = getattr(settings, 'GET_PROFILE_METHOD', None)
    if setting:
        method = load_member_from_setting('GET_PROFILE_METHOD')
        return method(user)

    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')

    # the models.get_model method allows to read load the model from the app's
    # model cache to allow the setting to be written as 'app_name.ModelName'
    profile_cls = models.get_model(app_label, model_name)
    return profile_cls.objects.create(user=user)
