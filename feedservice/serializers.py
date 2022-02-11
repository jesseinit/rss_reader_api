from rest_framework import serializers

from feedservice.models import Feed, FeedItems, ReadUnreadFeedItems


class StingOrIntField(serializers.Field):
    """Custom DRF Field that Accepts String and Integers"""

    def to_internal_value(self, data):
        if isinstance(data, int):
            return data
        elif isinstance(data, str):
            return data.lower()
        raise serializers.ValidationError(f"{data} is not a string or an integer")


class FeedInputSerializer(serializers.Serializer):
    url = serializers.URLField()


class FeedFollowUnfollowInputSerializer(serializers.Serializer):
    feed_ids = serializers.ListField(child=serializers.IntegerField())
    action = serializers.ChoiceField(choices=["follow", "unfollow"])

    def validate_feed_ids(self, feed_ids):
        return list(set(feed_ids))


class ReadUnreadQueryInputSerializer(serializers.Serializer):
    feed_id = serializers.IntegerField(required=False, min_value=1)
    status = serializers.ChoiceField(choices=["read", "unread"])

    def validate_feed_ids(self, feed_ids):
        return list(set(feed_ids))


class FeedDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = "__all__"


class FeedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItems
        fields = "__all__"


class ReadItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadUnreadFeedItems
        fields = "__all__"
