from typing import Dict, Type

from django.contrib.auth.hashers import check_password
from rest_framework import status
from userservice.models import User
from utils.helpers import CustomAPIException, FeedManager

from feedservice.models import Feed, FeedItems
from feedservice.serializers import FeedDetailsSerializer


class FeedService:
    def add_feed(url: str, creator: Type[User]) -> Dict:
        """Service method that handles feed creation"""
        # Todo - Add a hash to url to prevent same user duplicating already created feed
        feed_data = FeedManager.parse_feed_url(url)
        feed_instance = Feed.objects.create(title=feed_data.feed.title, url=url, registered_by=creator)

        # Automatically follow every feed that you create
        feed_instance.followers.add(creator)

        # Auto create feed items for the created feed
        feed_items = [
            FeedItems(title=item_data.title, link=item_data.link, summary=item_data.summary, feed=feed_instance)
            for item_data in feed_data.entries
        ]
        FeedItems.objects.bulk_create(feed_items, batch_size=500)

        return FeedDetailsSerializer(instance=feed_instance).data

    def retrieve_feed(feed_id: int, creator: Type[User]) -> Dict:
        feed_instance = Feed.objects.filter(id=feed_id, registered_by=creator).first()
        if feed_instance is None:
            raise CustomAPIException(
                "Feed not found",
                status.HTTP_404_NOT_FOUND,
            )
        return FeedDetailsSerializer(instance=feed_instance).data
