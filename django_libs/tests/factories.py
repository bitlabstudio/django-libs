"""
IMPORTANT: The following factories are still available, but no longer
maintained. We recommend to use https://github.com/klen/mixer for fixtures.

"""
from io import BytesIO
import warnings

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now

from hashlib import md5
from PIL import Image
from factory.django import DjangoModelFactory
import factory


class ParlerFactoryMixin(object):
    """
    Overrides ``_create`` and takes care of creating a translation.

    """
    def __new__(cls, **kwargs):
        warnings.warn(
            'Factories are deprecated and will be removed in django_libs>=2.0.'
            ' Please use https://github.com/klen/mixer instead.',
            DeprecationWarning)
        return super().__new__(**kwargs)


class UploadedImageFactory(object):
    """Creates an uploaded image for testing."""
    def __new__(cls, **kwargs):
        warnings.warn(
            'Factories are deprecated and will be removed in django_libs>=2.0.'
            ' Please use https://github.com/klen/mixer instead.',
            DeprecationWarning)
        return cls._create_image(**kwargs)

    @classmethod
    def _create_image(self, image_format='JPEG', filename='img.jpg'):
        thumb = Image.new('RGB', (100, 100), 'blue')
        thumb_io = BytesIO()
        thumb.save(thumb_io, format=image_format)
        self._image = SimpleUploadedFile(filename, thumb_io.getvalue())
        return self._image


class UserFactory(DjangoModelFactory):
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
    username = factory.Sequence(
        lambda n: md5(str(n).encode('utf-8')).hexdigest()[0:30]
    )
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))

    class Meta:
        model = User

    def __new__(cls, **kwargs):
        warnings.warn(
            'Factories are deprecated and will be removed in django_libs>=2.0.'
            ' Please use https://github.com/klen/mixer instead.',
            DeprecationWarning)
        return super(UserFactory, cls).__new__(**kwargs)

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


class SiteFactory(DjangoModelFactory):
    """
    Creates a new ``Site`` object.

    """
    name = factory.Sequence(lambda n: 'Example {}'.format(n))
    domain = factory.Sequence(lambda n: 'example{}.com'.format(n))

    class Meta:
        model = Site

    def __new__(cls, **kwargs):
        warnings.warn(
            'Factories are deprecated and will be removed in django_libs>=2.0.'
            ' Please use https://github.com/klen/mixer instead.',
            DeprecationWarning)
        return super(SiteFactory, cls).__new__(**kwargs)


try:
    from mailer.models import MessageLog
except ImportError:  # mailer not installed
    pass
else:
    class MessageLogFactory(DjangoModelFactory):
        """
        Creates a new ``MessageLog`` object.

        We only use this factory for testing purposes (management command:
        "cleanup_mailer_messagelog").

        """
        message_data = 'foo'
        when_added = factory.Sequence(lambda n: now())
        priority = '3'
        result = '1'
        log_message = 'foo'

        class Meta:
            model = MessageLog

        def __new__(cls, **kwargs):
            warnings.warn(
                'Factories are deprecated and will be removed in'
                ' django_libs>=2.0. Please use https://github.com/klen/mixer'
                ' instead.',
                DeprecationWarning)
            return super(MessageLogFactory, cls).__new__(**kwargs)
