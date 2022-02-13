from datetime import timezone

import factory
from userservice.tests.factories import UserFactory


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "feedservice.Feed"

    title = factory.Faker("sentence", nb_words=10)
    url = factory.Faker("url")
    registered_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date_time", tzinfo=timezone.utc)
    updated_at = factory.Faker("date_time", tzinfo=timezone.utc)

    @factory.post_generation
    def followers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for follower in extracted:
                self.followers.add(follower)
