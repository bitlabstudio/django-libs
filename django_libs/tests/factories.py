"""
Factories that are common to most Django apps.

The factories in this module shall help to create test fixtures for models that
are global to all Django projects and could be shared by tests of specialized
apps.

For example each app will need to create a user, therefore this module shall
provide facilities for user generation.

"""
from hashlib import md5

from django.contrib.auth.models import User

import factory


class HvadFactoryMixin(object):
    """
    Overrides ``_create`` and takes care of creating a translation.

    """
    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        obj = target_class(*args, **kwargs)

        # Factory boy and hvad behave a bit weird. When getting the object,
        # obj.some_translatable_field is actually set although no tranlsation
        # object exists, yet. We have to cache the translatable values ...
        cached_values = {}
        for field in obj._translated_field_names:
            if field in ['id', 'master', 'language_code']:
                continue
            cached_values[field] = getattr(obj, field)

        # ... because when calling translate, the translatable values will be
        # lost on the obj ...
        obj.translate(obj.language_code)
        for field in obj._translated_field_names:
            if field in ['id', 'master', 'language_code']:
                continue
            # ... so here we will put them back on the object, this time they
            # will be saved on the translatable object.
            setattr(obj, field, cached_values[field])

        obj.save()
        return obj


class SimpleTranslationMixin(object):
    """
    Adds a ``_prepare`` method that takes care of creating a translation.

    """

    @staticmethod
    def _get_translation_factory_and_field(self):
        """
        Should return a tuple of (TranslationFactory, 'fieldname').

        ``TranslationFactory`` is the factory class that can create translation
        objects for this objects.

        ``fieldname`` is the name of the FK on the translation class that
        points back to this object.

        """
        raise NotImplementedError()

    @classmethod
    def _prepare(cls, create, **kwargs):
        """
        Creates a ``PersonTranslation`` for this ``Person``.

        Note that we will only create a translation if you create a new object
        instead of just building it, because otherwise this object has no PK
        and cannot be used to instantiate the translation.

        """
        language = kwargs.pop('language', 'en')
        obj = super(SimpleTranslationMixin, cls)._prepare(create, **kwargs)
        if create:
            if language:
                translation_factory, fk_field = \
                    cls._get_translation_factory_and_field()
                kwargs_ = {
                    fk_field: obj,
                    'language': language,
                }
                translation_factory(**kwargs_)
        return obj


class UserFactory(factory.Factory):
    """
    Creates a new ``User`` object.

    We use ``django-registration-email`` which allows users to sign in with
    their email instead of a username. Since the username field is too short
    for most emails, we don't really use the username field at all and just
    store a md5 hash in there.

    Username will be a random 30 character md5 value.
    Email will be ``userN@example.com`` with ``N`` being a counter.
    Password will be ``test123`` by default.

    """
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: md5(str(n)).hexdigest()[0:30])
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = 'test123'
        if 'password' in kwargs:
            password = kwargs.pop('password')
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        user.set_password(password)
        if create:
            user.save()
        return user
