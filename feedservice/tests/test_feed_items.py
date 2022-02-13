import random
from typing import Tuple, Type

import pytest
from feedservice.tests.factories import FeedFactory, FeedItemsFactory, ReadUnreadFeedItemsFactory
from rest_framework import status
from userservice.tests.factories import UserFactory


@pytest.mark.django_db
class TestFeedItems:
    def create_read_unread_items_for_user(
        self,
        user_instance: Type[UserFactory] = None,
        item_size: int = 50,
    ) -> Tuple[int, int, int, int]:
        """Util test method to get user read/unread items counts"""

        # User one read and unread items
        feed = FeedFactory(registered_by=user_instance)
        feed_items = [FeedItemsFactory(feed=feed) for _ in range(item_size)]
        read_unread_items = [
            ReadUnreadFeedItemsFactory(
                user=user_instance, feed_item=feed_item, feed=feed, is_read=bool(random.getrandbits(1))
            )
            for feed_item in feed_items
        ]

        unread_items_count = len(list(filter(lambda item: item.is_read is False, read_unread_items)))
        read_items_count = len(list(filter(lambda item: item.is_read is True, read_unread_items)))

        return (
            feed.id,
            unread_items_count,
            read_items_count,
            len(feed_items),
        )

    def test_retrieve_a_feed_items(self, client, user_one_token):
        """Test that a user can retrieve a items belonging to a feed"""

        response = client.get("/api/v1/feed/10/items", **user_one_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["data"] == []

        feed = FeedFactory()
        total_count = 50
        page_size = 20
        [FeedItemsFactory(feed=feed) for _ in range(total_count)]

        response = client.get(f"/api/v1/feed/{feed.id}/items?page_size={page_size}", **user_one_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == total_count
        assert len(response_data["data"]) == page_size

    def test_retrieve_my_feed_items(self, client, user_two, user_one, user_one_token):
        """Test that a user can retrieve feed items belonging to feeds he has registered"""

        feed = FeedFactory(registered_by=user_two)
        total_count = 30
        [FeedItemsFactory(feed=feed) for _ in range(total_count)]

        # Before he registered the feed
        response = client.get("/api/v1/feed/my-feed-items", **user_one_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["data"] == []

        # After he registered the feed
        feed = FeedFactory(registered_by=user_one)
        total_count = 50
        [FeedItemsFactory(feed=feed) for _ in range(total_count)]

        page_size = 20
        response = client.get(f"/api/v1/feed/my-feed-items?page_size={page_size}", **user_one_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == total_count
        assert len(response_data["data"]) == page_size

    def test_retrieve_read_unread_feed_items_globally(self, client, user_two, user_one, user_two_token):
        """Test that a user can fetch ALL feed items he has read or unread"""

        # For Unread Count Globally
        _, _, _, user_one_feed_items_count = self.create_read_unread_items_for_user(user_instance=user_one)
        _, user_two_unread_items, user_two_read_items, _ = self.create_read_unread_items_for_user(
            user_instance=user_two
        )

        user_two_all_unread_items_count = user_two_unread_items + user_one_feed_items_count

        response = client.get(f"/api/v1/feed/items?status=unread", **user_two_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == user_two_all_unread_items_count

        # For Read Count Globally
        _, _, user_two_read_items_added, _ = self.create_read_unread_items_for_user(user_instance=user_two)

        response = client.get(f"/api/v1/feed/items?status=read", **user_two_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == user_two_read_items + user_two_read_items_added

    def test_retrieve_read_unread_feed_items_by_feed_id(self, client, user_two, user_one, user_two_token):
        """Test that a user can fetch feed items from a feed he has read or unread"""

        # Assert that a feed must exist before we can see results
        response = client.get(f"/api/v1/feed/items?status=unread&feed_id=30", **user_two_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["message"] == "Feed not found"

        # For Unread Count by feed_id
        feed_id, _, _, user_one_feed_items_count = self.create_read_unread_items_for_user(user_instance=user_one)

        response = client.get(f"/api/v1/feed/items?status=unread&feed_id={feed_id}", **user_two_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == user_one_feed_items_count

        # # # For Read Count by feed_id
        feed_id, _, user_two_read_items, _ = self.create_read_unread_items_for_user(user_instance=user_two)
        response = client.get(f"/api/v1/feed/items?status=read&feed_id={feed_id}", **user_two_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == user_two_read_items

    def test_mark_feed_item_read_unread(self, client, user_two, user_one, user_two_token):
        """Test that a user can mark an item as read or unread"""

        # Assert that a feed_item must exist before we can see results
        response = client.patch(f"/api/v1/feed/item/23473/read-unread", {}, **user_two_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["message"] == "Feed item not found"

        feed = FeedFactory(registered_by=user_one)
        total_count = 50
        feed_item_ids = [FeedItemsFactory(feed=feed).id for _ in range(total_count)]

        response = client.patch(
            f"/api/v1/feed/item/{random.choices(feed_item_ids)[0]}/read-unread", {}, **user_two_token
        )

        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["data"]["is_read"] is True
