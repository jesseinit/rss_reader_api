import time
from datetime import datetime as dt
from datetime import timezone
from email.utils import parsedate_to_datetime
from typing import Dict, List, Type, Union

import feedparser
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework import pagination, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from userservice.models import User


class CustomPagination(pagination.PageNumberPagination):
    """Custom Pagination Class"""

    def get_paginated_response(self, data):
        """Helper method the returns a response with pagination data"""
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        )


class ResponseManager:
    @staticmethod
    def handle_response(
        data: Union[Dict, List] = None,
        error: Union[Dict, List] = None,
        status: int = 200,
    ) -> Response:
        """Helper method to generate response object"""
        if error:
            return Response({"error": error}, status=status)
        return Response({"data": data}, status=status)


class CustomAPIException(APIException):
    """Custom Exception Class"""

    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "We are unable to process your request at this time. Please try again."

    def __init__(self, detail: Union[List, Dict, str], status_code: int = None) -> None:
        self.status_code = status_code if status_code else self.status_code
        message = detail if detail is not None else self.default_message
        self.detail = {"message": _(force_str(message))}


class TokenManager:
    """Utility class that abstracts interation with the token generation"""

    @classmethod
    def prepare_user_token(cls, user: Type[User]) -> Dict:
        """Helper method to generate user token"""
        token = RefreshToken.for_user(user)
        return {
            "user": user.id,
            "token": {"refresh": str(token), "access": str(token.access_token)},
        }


class FeedManager:
    """Utility class that manages helper methods for parsing feed"""

    @classmethod
    def parse_feed_url(cls, url: str) -> Dict:
        """Method to parse feed url"""
        feed_data = feedparser.parse(url)
        if feed_data.bozo is not False:
            raise CustomAPIException(
                _("Error parsing the provided feed url"), status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        return feed_data

    @classmethod
    def parse_feed_time(cls, feed_time: str, tz: Type[timezone] = timezone.utc) -> Type[dt]:
        """Utility method to parse feed or item time to datetime object"""
        return parsedate_to_datetime(feed_time)


class EmailManager:
    """Email Sender Class"""

    from_email = settings.EMAIL_FROM

    def __init__(self, email_body: str = None, subject: str = None, to_emails=[]):
        self.to_email = to_emails
        self.subject = subject
        self.body = email_body

    def _compose_mail(self):
        """Prepares the various mail parameters"""
        message = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            bcc=self.to_email,
        )
        message.content_subtype = "html"
        return message

    def send(self):
        """Mail send method"""
        mail = self._compose_mail()
        return mail.send(fail_silently=False)
