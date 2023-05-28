import factory
import factory.random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

SEED = 4321
PASSWORD = 'PswrdNmrc1'
HASHED_PASSWORD = make_password(PASSWORD)

factory.random.reseed_random(SEED)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    password = HASHED_PASSWORD
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')

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
