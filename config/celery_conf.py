from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(__name__)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.CELERYBEAT_SCHEDULE = {
    "update-feed-job": {
        "task": "feedservice.tasks.update_feed_and_items",
        "schedule": 60 * 30,  # Run every 30mins
    },
}
