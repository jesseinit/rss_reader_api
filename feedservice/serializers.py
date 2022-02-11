from rest_framework import serializers

from feedservice.models import Feed, FeedItems, ReadUnreadFeedItems


class FeedInputSerializer(serializers.Serializer):
    url = serializers.URLField()


class FeedFollowUnfollowInputSerializer(serializers.Serializer):
    feed_ids = serializers.ListField(child=serializers.IntegerField())
    action = serializers.ChoiceField(choices=["follow", "unfollow"])

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
