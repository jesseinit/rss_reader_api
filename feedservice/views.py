import utils.helpers as helpers
from rest_framework import status, viewsets
from rest_framework.decorators import action

import feedservice.serializers as serializers
import feedservice.service as services


class FeedViewset(viewsets.ViewSet):
    """Handles CRUD on the Feed Resource"""

    def create(self, request):
        """Register A Feed Resouce"""

        serialized_data = serializers.FeedInputSerializer(data=request.data)
        if not serialized_data.is_valid():
            return helpers.ResponseManager.handle_response(
                message="Something wrong with the data that has been provided",
                error=serialized_data.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        service_response = services.FeedService.add_feed(url=serialized_data.data["url"], creator=request.user)
        return helpers.ResponseManager.handle_response(
            message="Feed Added", data=service_response, status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        """Fetch User Feeds"""
        service_response = services.FeedService.fetch_registered_feeds(creator=request.user)
        return helpers.ResponseManager.handle_response(
            message="Feed Retrieved", data=service_response, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"], url_path="(?P<feed_id>[0-9]+)/items")
    def retrieve_a_feed_items(self, request, *args, **kwargs):
        """Fetch A Feed's Items"""
        service_response = services.FeedService.retrieve_feed_items(feed_id=int(kwargs["feed_id"]))
        return helpers.ResponseManager.handle_response(
            message="Feed Items Retrieved", data=service_response, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"], url_path="my-feed-items")
    def retrieve_my_feed_items(self, request, *args, **kwargs):
        """Fetch User Feed's Items"""
        service_response = services.FeedService.retrieve_feed_items(creator=request.user)
        return helpers.ResponseManager.handle_response(
            message="Feed Items Retrieved", data=service_response, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["patch"], url_path="item/(?P<feed_item_id>[0-9]+)/read-unread")
    def handle_feed_read_state(self, request, *args, **kwargs):
        """Hanles Feed Reading"""
        service_response = services.FeedService.mark_read_unread(
            feed_item_id=kwargs.get("feed_item_id"), creator=request.user
        )
        return helpers.ResponseManager.handle_response(
            message="Feed Item Read Status Updated", data=service_response, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["patch"], url_path="follow-unfollow")
    def handle_feed_follow_state(self, request, *args, **kwargs):
        """Hanles Feed Following/Unfollowing"""

        serialized_data = serializers.FeedFollowUnfollowInputSerializer(data=request.data)
        if not serialized_data.is_valid():
            return helpers.ResponseManager.handle_response(
                message="Something wrong with the data that has been provided",
                error=serialized_data.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        service_response = services.FeedService.follow_unfollow_feed(
            feed_ids=serialized_data.data["feed_ids"], action=serialized_data.data["action"], creator=request.user
        )
        return helpers.ResponseManager.handle_response(
            message="Feed Item Follow Status Updated", data=service_response, status=status.HTTP_200_OK
        )
