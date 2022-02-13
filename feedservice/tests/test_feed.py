import pytest
from conftest import DotDict
from feedservice.tests.factories import FeedFactory
from rest_framework import status


@pytest.mark.django_db
class TestFeed:
    def test_authenticated_resource(self, client):
        """Test that the feed resouces are all protected"""
        responses = [
            client.get("/api/v1/feed", content_type="application/json"),
            client.post("/api/v1/feed", {}, content_type="application/json"),
            client.patch("/api/v1/feed/follow-unfollow", {}, content_type="application/json"),
            client.patch("/api/v1/feed/1/force-update", {}, content_type="application/json"),
        ]

        status_codes = [res.status_code for res in responses]
        assert all(code == status.HTTP_401_UNAUTHORIZED for code in status_codes)

    def test_add_feed_url_with_bad_inputs(self, client, user_one_token):
        """Test for adding a feed url with unprocessible input inputs"""
        response = client.post("/api/v1/feed", {"url": "nunl/rss/Algemeen"}, **user_one_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data["error"]["url"][0] == "Enter a valid URL."

    def test_add_feed_url_with_invalid_url(self, client, mocker, user_one, user_one_token, feed_response):
        """Test for errors when adding a feed url that is not valid"""

        mocker.patch("utils.helpers.feedparser.parse", return_value=DotDict({"bozo": True}))

        response = client.post("/api/v1/feed", {"url": "http://www.nu.nl/rss/Algemeen"}, **user_one_token)

        response_data = response.json()
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response_data["message"] == "Error parsing the provided feed url"

    def test_add_feed_url_success(self, client, mocker, user_one, user_one_token, feed_response):
        """Test for adding a feed url by authenticated users"""

        mocker.patch("feedservice.service.FeedManager.parse_feed_url", return_value=feed_response)

        response = client.post("/api/v1/feed", {"url": "http://www.nu.nl/rss/Algemeen"}, **user_one_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert user_one.id in response_data["data"]["followers"]

    def test_fetch_my_feeds(self, client, user_one, user_two, user_one_token):
        """Test that users can fetch their feed items and also see those following them"""
        FeedFactory.create(
            registered_by=user_one,
            followers=(
                user_one,
                user_two,
            ),
        )
        response = client.get("/api/v1/feed", **user_one_token)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == 1
        assert len(response_data["data"]) == 1
        assert len(response_data["data"][0]["followers"]) == 2

    def test_follow_unfollow_non_existing_feeds(self, client, user_one, user_one_token):
        """Test that users cannot follow/unfollow non-existing feeds"""

        payload = {"action": "follow", "feed_ids": [20, 15, 44]}
        response = client.patch("/api/v1/feed/follow-unfollow", payload, **user_one_token)

        response_data = response.json()

        # Assert that user cannot follow feeds that dont exist
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["message"] == f"Feeds not found"

    def test_follow_unfollow_feed(self, client, user_one, user_two, user_one_token):
        """Test that users can follow/unfollow single or multiple feeds"""
        feeds = FeedFactory.create_batch(size=3)
        feeds_ids = [feed.id for feed in feeds]

        payload = {"feed_ids": feeds_ids, "action": "unfollow"}
        response = client.patch("/api/v1/feed/follow-unfollow", payload, **user_one_token)
        response_data = response.json()

        # Assert that user has NOT unfollowed feeds he is intends following
        assert response_data["data"]["message"] == "Unfollowed 0 feed(s)"

        payload["action"] = "follow"
        response = client.patch("/api/v1/feed/follow-unfollow", payload, **user_one_token)
        response_data = response.json()

        # Assert that user HAS followed feeds he intend following
        assert response_data["data"]["message"] == f"Followed {len(payload['feed_ids'])} feed(s)"

        payload["action"] = "unfollow"
        response = client.patch("/api/v1/feed/follow-unfollow", payload, **user_one_token)
        response_data = response.json()

        # Assert that same user HAS unfollowed feeds he WAS following
        assert response_data["data"]["message"] == f"Unfollowed {len(payload['feed_ids'])} feed(s)"

    def test_force_a_feed_update(self, mocker, client, user_one_token):
        """Test that users can force the update of a feed"""
        bg_task_mock = mocker.patch("feedservice.tasks.update_feed_and_items.delay")

        response = client.patch(f"/api/v1/feed/{20}/force-update", {}, **user_one_token)
        response_data = response.json()

        # Asset that non-exisiting feed cannot be force updated
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["message"] == "Feed not found"
        assert bg_task_mock.call_count == 0

        feed = FeedFactory()
        response = client.patch(f"/api/v1/feed/{feed.id}/force-update", {}, **user_one_token)
        response_data = response.json()

        assert response_data["data"] == f"Feed update has been triggered. Timeline would be updated shortly"
        assert bg_task_mock.call_count == 1
