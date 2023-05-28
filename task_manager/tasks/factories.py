import factory
import factory.random
from factory.django import DjangoModelFactory

from .models import Task

SEED = 4321
factory.random.reseed_random(SEED)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    status = None
    executor = None
    assigned_by = None

    @factory.post_generation  # handlind M2M field
    def labels(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            # Add labels to the task
            for label in extracted:
                self.labels.add(label)

    @classmethod
    def create_fake_task(cls, **kwargs):
        user = cls.build()
        return {
            'name': user.name,
            'description': user.description,
            'status': kwargs.get('status', ""),
            'executor': kwargs.get('executor', ""),
            'assigned_by': kwargs.get('assigned_by', ""),
            'labels': kwargs.get('labels', ""),
        }
