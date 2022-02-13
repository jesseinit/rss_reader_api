from tkinter import E
from typing import Dict, List, Literal, Type, Union

from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from feedparser.util import FeedParserDict
from rest_framework import status
from userservice.models import User
from utils.helpers import CustomAPIException, FeedManager

from feedservice.models import Feed, FeedItems, ReadUnreadFeedItems
from feedservice.serializers import FeedDetailsSerializer, ReadItemsSerializer


class FeedService:
    """Service container class with utility methods with business logic"""

    @transaction.atomic
    def add_feed(url: str, creator: Type[User]) -> Dict:
        """Service method that handles feed creation"""
        feed_instance = Feed.objects.filter(url=url).first()
        if feed_instance:
            feed_instance.followers.add(creator)
            return FeedDetailsSerializer(instance=feed_instance).data

        feed_data = FeedManager.parse_feed_url(url)

        feed_instance = Feed.objects.create(
            title=feed_data.feed.title,
            url=url,
            registered_by=creator,
            updated_at=FeedManager.parse_feed_time(feed_data.feed.updated),
        )

        # Automatically follow every feed that you create
        feed_instance.followers.add(creator)

        FeedService.create_feed_items_from_entries(entries=feed_data.entries, feed_id=feed_instance.id)

        return FeedDetailsSerializer(instance=feed_instance).data

    def retrieve_feed_items(feed_id: int = None, creator: Type[User] = None):
        """Get feed items either by an id or those created by a user"""
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
        return feed_item_qs

    def fetch_registered_feeds(creator: Type[User] = None) -> Dict:
        """Retrieves feeds registered by the authenticated user"""
        return Feed.objects.filter(registered_by=creator)

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
            return {"message": _(f"Unfollowed {feed_count} feed(s)")}

        if action == "follow":
            for feed in feed_instances:
                if feed.id not in user_feed_ids:
                    feed.followers.add(creator)
                    feed_count += 1
            return {"message": _(f"Followed {feed_count} feed(s)")}

    def retrieve_feed_all_items_with_query_filtering(
        status: Literal["read", "unread"] = None, feed_id: Union[int, None] = None, creator: Type[User] = None
    ):
        """Handles the querying of a user's read or unread feed items"""

        feed_item_qs = ReadUnreadFeedItems.objects.filter(user=creator, is_read=True)

        if feed_id:
            feed_instance = Feed.objects.filter(id=feed_id).exists()
            if feed_instance is False:
                raise CustomAPIException(
                    "Feed not found",
                    404,
                )

            feed_item_qs = feed_item_qs.filter(feed_id=feed_id)

        # Unread - Get the feed_item that are not in ReadUnreadFeedItems from FeedItems for a specific feed
        # Read - Get the ids he has read then fetch only those

        if status == "read":
            final_qs = FeedItems.objects.filter(id__in=feed_item_qs.values_list("feed_item_id", flat=True))
        if status == "unread":
            final_qs = FeedItems.objects.filter(
                ~Q(id__in=feed_item_qs.values_list("feed_item_id", flat=True)), (Q(feed_id=feed_id) if feed_id else Q())
            )

        return final_qs

    def feed_force_update(feed_id: str = None) -> str:
        """Service method that handles force updating of a feed"""
        import feedservice.tasks as Tasks

        feed = Feed.objects.filter(id=feed_id).first()
        if feed is None:
            raise CustomAPIException("Feed not found", status_code=status.HTTP_404_NOT_FOUND)

        Tasks.update_feed_and_items.delay(feed_id=feed_id)

        return "Feed update has been triggered triggered. Timeline would be updated shortly"

    def create_feed_items_from_entries(entries: List[FeedParserDict], feed_id: int) -> List[Type[FeedItems]]:
        """Create feeditems from parsed feed entries"""
        feed_items = [
            FeedItems(
                title=item_data.title,
                link=item_data.link,
                summary=item_data.summary,
                feed_id=feed_id,
                published_at=FeedManager.parse_feed_time(item_data.published),
                entry_id=item_data.id,
            )
            for item_data in entries
        ]
        return FeedItems.objects.bulk_create(feed_items)
