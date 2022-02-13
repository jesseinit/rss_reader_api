import factory

# from django.contrib.auth.hashers import make_password
from faker import Factory as FakerFactory


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "feedservice.Feed"

    title = factory.Faker("sentence", sentence=10)
    url = factory.Faker("url")
    email = factory.Faker("email")
    created_at = factory.Faker("email")
    updated_at = factory.Faker("email")
