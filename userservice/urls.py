from django.conf.urls import re_path, url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

import userservice.views as views

router = DefaultRouter(trailing_slash=False)
router.register(r"auth", views.UserOnboardingViewset, basename="bvn-user-onboarding")

urlpatterns = [
    re_path(r"", include(router.urls)),
]
