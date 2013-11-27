"""Just some factories for the test app."""
import factory

from ..factories import UserFactory
from models import DummyProfile, DummyProfileTranslation


class DummyProfileFactory(factory.DjangoModelFactory):
    """Factory for the ``DummyProfile`` model."""
    FACTORY_FOR = DummyProfile

    user = factory.SubFactory(UserFactory)
    dummy_field = factory.Sequence(lambda n: 'dummyfield{}'.format(n))


class DummyProfileTranslationFactory(factory.DjangoModelFactory):
    """Factory for the ``DummyProfileTranslation`` model."""
    FACTORY_FOR = DummyProfileTranslation

    dummy_translation = factory.Sequence(lambda n: 'trans {}'.format(n))
    dummyprofile = factory.SubFactory(DummyProfileFactory)
