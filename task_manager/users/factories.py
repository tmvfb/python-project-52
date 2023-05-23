import factory
import factory.random
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User


SEED = 4321
PASSWORD = 'PswrdNmrc1'

factory.random.reseed_random(SEED)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    # this password definition makes tests slow but is crucial for login testing
    password = factory.PostGenerationMethodCall('set_password', PASSWORD)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('word')

    @classmethod
    def create_fake_user(cls, **kwargs):
        user = cls.build()
        return {
            'password1': kwargs.get('password', PASSWORD),
            'password2': kwargs.get('password', PASSWORD),
            'first_name': kwargs.get('first_name', user.first_name),
            'last_name': kwargs.get('last_name', user.last_name),
            'username': kwargs.get('username', user.username),
        }
