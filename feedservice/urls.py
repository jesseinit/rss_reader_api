from django.conf.urls import re_path, url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

import feedservice.views as views

router = DefaultRouter(trailing_slash=False)
router.register(r"feed", views.FeedViewset, basename="feed-resource")

urlpatterns = [
    re_path(r"", include(router.urls)),
]
