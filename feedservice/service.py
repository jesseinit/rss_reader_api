from typing import Dict, Type

from django.contrib.auth.hashers import check_password
from rest_framework import status
from userservice.models import User
from utils.helpers import CustomAPIException, FeedManager

from feedservice.models import Feed, FeedItems
from feedservice.serializers import FeedDetailsSerializer, FeedItemsSerializer


class FeedService:
    def add_feed(url: str, creator: Type[User]) -> Dict:
        """Service method that handles feed creation"""

        feed_instance = Feed.objects.filter(url=url).first()
        if feed_instance:
            feed_instance.followers.add(creator)
            return FeedDetailsSerializer(instance=feed_instance).data

        feed_data = FeedManager.parse_feed_url(url)
        feed_instance = Feed.objects.create(title=feed_data.feed.title, url=url, registered_by=creator)

        # Automatically follow every feed that you create
        feed_instance.followers.add(creator)

        feed_items = [
            FeedItems(title=item_data.title, link=item_data.link, summary=item_data.summary, feed=feed_instance)
            for item_data in feed_data.entries
        ]
        FeedItems.objects.bulk_create(feed_items, batch_size=500)

        return FeedDetailsSerializer(instance=feed_instance).data

    def my_retrieve_feeds(creator: Type[User] = None) -> Dict:
        feed_instance = Feed.objects.filter(registered_by=creator).first()
        if feed_instance is None:
            raise CustomAPIException(
                "Feed not found",
                status.HTTP_404_NOT_FOUND,
            )
        feed_item_qs = FeedItems.objects.filter(feed_id=feed_instance.id)
        return FeedItemsSerializer(instance=feed_item_qs, many=True).data

    def retrieve_feed_items(creator: Type[User] = None) -> Dict:
        feed_instance = Feed.objects.filter(registered_by=creator)
        if feed_instance is None:
            raise CustomAPIException(
                "Feed not found",
                status.HTTP_404_NOT_FOUND,
            )
        feed_item_qs = FeedItems.objects.filter(feed__in=feed_instance)
        return FeedItemsSerializer(instance=feed_item_qs, many=True).data

    def fetch_registered_feeds(creator: Type[User] = None) -> Dict:
        feed_instance = Feed.objects.filter(registered_by=creator)
        return FeedDetailsSerializer(instance=feed_instance, many=True).data
