"""Just some factories for the test app."""
import factory

from ..factories import DjangoModelFactory, ParlerFactoryMixin, UserFactory
from .models import DummyProfile, ParlerDummy


class ParlerDummyFactory(ParlerFactoryMixin, DjangoModelFactory):
    """Factory for the ``HvadDummy`` model."""
    title = factory.Sequence(lambda n: 'title{}'.format(n))

    class Meta:
        model = ParlerDummy


class DummyProfileFactory(DjangoModelFactory):
    """Factory for the ``DummyProfile`` model."""
    user = factory.SubFactory(UserFactory)
    dummy_field = factory.Sequence(lambda n: 'dummyfield{}'.format(n))

    class Meta:
        model = DummyProfile
