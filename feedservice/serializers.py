from rest_framework import serializers

from feedservice.models import Feed


class FeedInputSerializer(serializers.Serializer):
    url = serializers.URLField()


class FeedDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = "__all__"
