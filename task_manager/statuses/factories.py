import factory
import factory.random
from factory.django import DjangoModelFactory

from .models import Status

SEED = 4321
factory.random.reseed_random(SEED)


class StatusFactory(DjangoModelFactory):
    class Meta:
        model = Status

    name = factory.Faker('word')
