from django.db import models


# Create your models here.
class Feed(models.Model):
    """Feed Model"""

    title = models.CharField(max_length=225)
    url = models.URLField(max_length=225, unique=True)
    registered_by = models.ForeignKey("userservice.User", related_name="my_feeds", on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField("userservice.User", related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, null=True)

    def __str__(self) -> str:
        return f"Feed<{self.rss_url}>"


class FeedItems(models.Model):
    """Feed Model"""

    title = models.CharField(max_length=225)
    link = models.TextField()
    summary = models.TextField()
    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f"ID:{self.id} title: {self.title}"


class ReadUnreadFeedItems(models.Model):
    """Read and Unread FeedItems Model"""

    user = models.ForeignKey("userservice.User", on_delete=models.CASCADE)
    feed_item = models.ForeignKey(FeedItems, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "is_read",
                ]
            )
        ]

    def __str__(self):
        return f"ID:{self.id} is_read: {self.is_read} user: {self.user}"
