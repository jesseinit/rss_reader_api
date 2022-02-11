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

    def retrieve(self, request, *args, **kwargs):
        """Get a Feed Resouce"""
        service_response = services.FeedService.retrieve_feed(feed_id=kwargs.get("pk"), creator=request.user)
        return helpers.ResponseManager.handle_response(
            message="Feed Retrieved", data=service_response, status=status.HTTP_200_OK
        )
