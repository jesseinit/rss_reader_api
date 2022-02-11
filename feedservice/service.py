from typing import Dict, List, Literal, Type

from django.contrib.auth.hashers import check_password
from rest_framework import status
from userservice.models import User
from utils.helpers import CustomAPIException, FeedManager

from feedservice.models import Feed, FeedItems, ReadUnreadFeedItems
from feedservice.serializers import FeedDetailsSerializer, FeedItemsSerializer, ReadItemsSerializer


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

    def retrieve_feed_items(feed_id: int = None, creator: Type[User] = None) -> Dict:
        if creator and not feed_id:
            feed_instance = Feed.objects.filter(registered_by=creator)
        if feed_id and not creator:
            feed_instance = Feed.objects.filter(id=feed_id)

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

    def mark_read_unread(feed_item_id: int, creator: Type[User] = None) -> Dict:
        """Handles processing of read state for a feed item"""
        feed_item_instance = FeedItems.objects.select_related("feed").filter(id=feed_item_id).first()
        if feed_item_instance is None:
            raise CustomAPIException(
                "Feed item not found",
                status.HTTP_404_NOT_FOUND,
            )

        read_unread_feed_item = ReadUnreadFeedItems.objects.filter(feed_item=feed_item_instance, user=creator).first()
        if read_unread_feed_item is None:
            # Item has not been read, so create and set as read
            read_unread_feed_item = ReadUnreadFeedItems.objects.create(
                feed_item=feed_item_instance, feed_id=feed_item_instance.feed.id, user=creator, is_read=True
            )
            return ReadItemsSerializer(instance=read_unread_feed_item).data

        # Item has not been read, so create and set as read
        if read_unread_feed_item.is_read is True:
            read_unread_feed_item.is_read = False
        else:
            read_unread_feed_item.is_read = True

        read_unread_feed_item.save(update_fields=["is_read"])

        return ReadItemsSerializer(instance=read_unread_feed_item).data

    def follow_unfollow_feed(
        feed_ids: List[int], action: Literal["follow", "unfollow"] = None, creator: Type[User] = None
    ) -> Dict:
        """Handles following and unfollowing of a feed item"""
        feed_instances = Feed.objects.filter(id__in=feed_ids)
        if not len(feed_instances):
            raise CustomAPIException(
                "Feeds not found",
                status.HTTP_404_NOT_FOUND,
            )

        user = User.objects.prefetch_related("my_feeds").get(id=creator.id)
        user_feed_ids = list(user.my_feeds.all().values_list("id", flat=True))

        feed_count = 0
        if action == "unfollow":
            for feed in feed_instances:
                if feed.id in user_feed_ids:
                    feed.followers.remove(creator)
                    feed_count += 1
            return {"message": f"Unfollowed {feed_count} feed(s)"}

        if action == "follow":
            for feed in feed_instances:
                if feed.id not in user_feed_ids:
                    feed.followers.add(creator)
                    feed_count += 1
            return {"message": f"Followed {feed_count} feed(s)"}
