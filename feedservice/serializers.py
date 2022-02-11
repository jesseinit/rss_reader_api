from rest_framework import serializers

from feedservice.models import Feed, FeedItems


class FeedInputSerializer(serializers.Serializer):
    url = serializers.URLField()


class FeedDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ("id", "title", "url", "registered_by", "created_at", "updated_at")


class FeedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItems
        fields = "__all__"
