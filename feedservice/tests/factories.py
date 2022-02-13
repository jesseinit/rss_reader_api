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


class FeedItemsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "feedservice.FeedItems"

    title = factory.Faker("sentence", nb_words=10)
    link = factory.Faker("url")
    summary = factory.Faker("sentence", nb_words=100)
    feed = factory.SubFactory(FeedFactory)
    created_at = factory.Faker("date_time", tzinfo=timezone.utc)
    published_at = factory.Faker("date_time", tzinfo=timezone.utc)
    entry_id = factory.Faker("uuid4")


class ReadUnreadFeedItemsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "feedservice.ReadUnreadFeedItems"

    user = factory.SubFactory(UserFactory)
    feed_item = factory.SubFactory(FeedItemsFactory)
    feed = factory.SubFactory(FeedItemsFactory)
    is_read = factory.Faker("boolean")
