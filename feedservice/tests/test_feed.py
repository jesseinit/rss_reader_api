# Create Feed
# Follow/UnFollow Feed
# My registered Feed

import pytest
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.usefixtures("celery_session_app")
@pytest.mark.usefixtures("celery_session_worker")
class TestFeed:
    def test_add_feed_url_success(self, client, mocker, user_one, user_one_token, feed_response):
        """Test for adding a feed url by authenticated users"""

        mocker.patch("feedservice.service.FeedManager.parse_feed_url", return_value=feed_response)

        response = client.post(
            "/api/v1/feed", {"url": "http://www.nu.nl/rss/Algemeen"}, content_type="application/json", **user_one_token
        )
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert user_one.id in response_data["data"]["followers"]

    def test_add_feed_url_success(self, client, mocker, user_one, user_one_token, feed_response):
        """Test for adding a feed url by authenticated users"""
