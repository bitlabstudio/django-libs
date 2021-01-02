"""Just some factories for the test app."""
import factory

from ..factories import DjangoModelFactory, HvadFactoryMixin, UserFactory
from .models import DummyProfile, HvadDummy


class HvadDummyFactory(HvadFactoryMixin, DjangoModelFactory):
    """Factory for the ``HvadDummy`` model."""
    title = factory.Sequence(lambda n: 'title{}'.format(n))

    class Meta:
        model = HvadDummy


class DummyProfileFactory(DjangoModelFactory):
    """Factory for the ``DummyProfile`` model."""
    user = factory.SubFactory(UserFactory)
    dummy_field = factory.Sequence(lambda n: 'dummyfield{}'.format(n))

    class Meta:
        model = DummyProfile
