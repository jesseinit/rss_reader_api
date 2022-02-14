import logging

from celery import shared_task
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from userservice.models import User
from utils.helpers import EmailManager, FeedManager

import feedservice.service as fs
from feedservice.models import Feed, FeedItems

logging.basicConfig(level=logging.DEBUG)


def notify_users(self, exc, task_id, args, kwargs, einfo):
    """Notify user callback function"""

    user_emails = User.objects.values_list("email", flat=True)
    mail = EmailManager(
        email_body=_(f"The feed has failed to update"),
        subject="Failed Feed Update",
        to_emails=user_emails,
    )
    mail.send()


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    max_retries=settings.CELERY_MAX_RETRY,
    retry_backoff=True,
    retry_jitter=False,
    on_failure=notify_users,
)
def update_feed_and_items(self, feed_id: int = None):
    """Background task to update single or multiple feeds"""

    if feed_id:
        feed_qs = Feed.objects.filter(id=feed_id)
        if not len(feed_qs):
            return "Feed not found"
    else:
        feed_qs = Feed.objects.all()

    # Fetch records in chuncks.
    for feed in feed_qs.iterator(chunk_size=1 if not feed_id else 1000):
        logging.info(f"Fetching feed data from {feed.url}.")
        feed_data = FeedManager.parse_feed_url(feed.url)
        feed_resource_last_update = FeedManager.parse_feed_time(feed_data.updated)

        feed_record_last_update = feed.updated_at
        is_update_due = feed_resource_last_update > feed_record_last_update
        if is_update_due:
            feed.title = feed_data.feed.title
            feed.updated_at = feed_resource_last_update
            feed.save(update_fields=["title", "updated_at"])

        feed_items = list(FeedItems.objects.filter(feed=feed).values("entry_id", "published_at"))

        if len(feed_items) < 1:
            # This is for a case where the feed didn't have items when it was first added, we update here.
            created_feed_items = fs.FeedService.create_feed_items_from_entries(
                entries=feed_data.entries, feed_id=feed.id
            )
            logging.info(f"Added {len(created_feed_items)} new feed items from {feed.url}.")
            continue

        most_recent_feed_item = feed_items[0]
        all_entry_ids = [entry_id["entry_id"] for entry_id in feed_items]

        # We check that only items that has not been added before are added
        filtered_entried = [
            item_data
            for item_data in feed_data.entries
            if FeedManager.parse_feed_time(item_data.published) > most_recent_feed_item["published_at"]
            and item_data.id not in all_entry_ids
        ]

        created_feed_items = fs.FeedService.create_feed_items_from_entries(entries=filtered_entried, feed_id=feed.id)

        logging.info(f"Added {len(created_feed_items)} new feed items from {feed.url}.")

    logging.info(f"Feed update completed, We're up to speed now! Phewwww!!!")
