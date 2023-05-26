import factory
import factory.random
from factory.django import DjangoModelFactory
from .models import Label


SEED = 4321
factory.random.reseed_random(SEED)


class LabelFactory(DjangoModelFactory):
    class Meta:
        model = Label

    name = factory.Faker('word')
