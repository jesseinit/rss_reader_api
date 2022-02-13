import utils.docs_spec as schema_spec
import utils.helpers as helpers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

import feedservice.serializers as serializers
import feedservice.service as services


class FeedViewset(viewsets.ViewSet):
    """Handles CRUD on the Feed Resource"""

    pagination_class = helpers.CustomPagination()

    @swagger_auto_schema(
        operation_summary="Register A Feed Resouce",
        tags=["Feed"],
        request_body=serializers.FeedInputSerializer,
        responses=schema_spec.ONBOARDING_REGISTER_RESPONSES,
    )
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
        return helpers.ResponseManager.handle_response(data=service_response, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """Fetch all User Feeds"""
        regsitered_feeds_qs = services.FeedService.fetch_registered_feeds(creator=request.user)
        paginated_queryset = self.pagination_class.paginate_queryset(regsitered_feeds_qs, request)
        service_response = serializers.FeedDetailsSerializer(instance=paginated_queryset, many=True).data
        return self.pagination_class.get_paginated_response(service_response)

    @action(detail=False, methods=["get"], url_path="(?P<feed_id>[0-9]+)/items")
    def retrieve_a_feed_items(self, request, *args, **kwargs):
        """Fetch A Feed's Items"""
        feed_items_qs = services.FeedService.retrieve_feed_items(feed_id=int(kwargs["feed_id"]))
        paginated_queryset = self.pagination_class.paginate_queryset(feed_items_qs, request)
        service_response = serializers.FeedItemsSerializer(instance=paginated_queryset, many=True).data
        return self.pagination_class.get_paginated_response(service_response)

    @action(detail=False, methods=["get"], url_path="items")
    def retrieve_all_feed_items(self, request, *args, **kwargs):
        """Fetch All Feed Items"""
        serialized_data = serializers.ReadUnreadQueryInputSerializer(data=request.query_params)
        if not serialized_data.is_valid():
            return helpers.ResponseManager.handle_response(
                message="Something wrong with the data that has been provided",
                error=serialized_data.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        feed_items_qs = services.FeedService.retrieve_feed_all_items_with_query_filtering(
            feed_id=serialized_data.data.get("feed_id"),
            status=serialized_data.data.get("status"),
            creator=request.user,
        )
        paginated_queryset = self.pagination_class.paginate_queryset(feed_items_qs, request)
        service_response = serializers.FeedItemsSerializer(instance=paginated_queryset, many=True).data
        return self.pagination_class.get_paginated_response(service_response)

    @action(detail=False, methods=["get"], url_path="my-feed-items")
    def retrieve_my_feed_items(self, request, *args, **kwargs):
        """Fetch User Feed's Items"""
        feed_items_qs = services.FeedService.retrieve_feed_items(creator=request.user)
        paginated_queryset = self.pagination_class.paginate_queryset(feed_items_qs, request)
        service_response = serializers.FeedItemsSerializer(paginated_queryset, many=True).data
        paginated_response = self.pagination_class.get_paginated_response(service_response)
        return paginated_response

    @action(detail=False, methods=["patch"], url_path="item/(?P<feed_item_id>[0-9]+)/read-unread")
    def handle_feed_read_state(self, request, *args, **kwargs):
        """Handles Feed Reading"""
        service_response = services.FeedService.mark_read_unread(
            feed_item_id=kwargs.get("feed_item_id"), creator=request.user
        )
        return helpers.ResponseManager.handle_response(data=service_response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="follow-unfollow")
    def handle_feed_following(self, request, *args, **kwargs):
        """Handles Feed Following/Unfollowing"""

        serialized_data = serializers.FeedFollowUnfollowInputSerializer(data=request.data)
        if not serialized_data.is_valid():
            return helpers.ResponseManager.handle_response(
                error=serialized_data.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        service_response = services.FeedService.follow_unfollow_feed(
            feed_ids=serialized_data.data["feed_ids"], action=serialized_data.data["action"], creator=request.user
        )
        return helpers.ResponseManager.handle_response(data=service_response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="(?P<feed_id>[0-9]+)/force-update")
    def force_update_feed(self, request, *args, **kwargs):
        """Feed Force Update"""
        service_response = services.FeedService.feed_force_update(feed_id=int(kwargs["feed_id"]))
        return helpers.ResponseManager.handle_response(data=service_response, status=status.HTTP_200_OK)
