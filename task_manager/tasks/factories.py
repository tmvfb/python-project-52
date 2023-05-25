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
    description = factory.Faker('word')
    status = None
    assigned_to = None
    assigned_by = None

    @classmethod
    def create_fake_task(cls, **kwargs):
        user = cls.build()
        return {
            'name': user.name,
            'description': user.description,
            'status': kwargs['status'],
            'assigned_to': kwargs['assigned_to'],
            'assigned_by': kwargs['assigned_by'],
        }
