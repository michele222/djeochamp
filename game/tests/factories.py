import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from game.models import Country, Championship, Parameter, CountryParameter


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n:04}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")
    password = factory.LazyFunction(lambda: make_password('password'))


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Championship

    title = factory.Faker('sentence', nb_words=4)
    user = factory.SubFactory(UserFactory)


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    id = factory.Sequence(lambda n: '%03d' % n)
    name = factory.Faker('pystr', max_chars=40)


class ParameterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parameter

    name = factory.Sequence(lambda n: 'parameter%d' % n)
    active = True


class CountryParameterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CountryParameter

    country = factory.SubFactory(CountryFactory)
    parameter = factory.SubFactory(ParameterFactory)
    value = factory.Faker('pyint', min_value=0, max_value=1000000)
