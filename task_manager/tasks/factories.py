import factory
import factory.random
from factory.django import DjangoModelFactory
from .models import Task


SEED = 4321
factory.random.reseed_random(SEED)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Faker('word')
