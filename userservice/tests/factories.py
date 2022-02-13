import factory
from django.contrib.auth.hashers import make_password
from faker import Factory as FakerFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "userservice.User"

    username = factory.Faker("username")
    password = factory.LazyFunction(lambda: make_password("K1#EzbuXsFWZ"))
    email = factory.Faker("email")
