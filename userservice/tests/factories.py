import factory
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "userservice.User"

    username = factory.Faker("user_name")
    password = factory.LazyFunction(lambda: make_password("K1#EzbuXsFWZ"))
    email = factory.Faker("ascii_company_email")
