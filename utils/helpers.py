from typing import Dict, List, Type, Union

from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from userservice.models import User
import feedparser


class ResponseManager:
    @staticmethod
    def handle_response(
        message: str = None,
        data: Union[Dict, List] = None,
        error: Union[Dict, List] = None,
        status: int = 200,
    ) -> Response:
        if error:
            return Response({"message": message, "data": None, "error": error}, status=status)
        return Response({"message": message, "data": data, "error": None}, status=status)


class CustomAPIException(APIException):
    """Custom Exception Class"""

    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "We are unable to process your request at this time. Please try again."

    def __init__(self, detail: Union[List, Dict, str], status_code: int) -> None:
        self.status_code = status_code if status_code else self.status_code
        message = detail if detail is not None else self.default_message
        self.detail = {"message": force_str(message)}


class TokenManager:
    """Utility class that abstracts interation with the token generation"""

    @classmethod
    def prepare_user_token(cls, user: Type[User]) -> Dict:
        token = RefreshToken.for_user(user)
        return {
            "user": user.id,
            "token": {"refresh": str(token), "access": str(token.access_token)},
        }


class FeedManager:
    """Utility class that abstracts interation with the caching engine"""

    @classmethod
    def parse_feed_url(cls, url: str) -> Dict:
        feed_data = feedparser.parse(url)
        if feed_data.bozo is not False:
            raise CustomAPIException("Error parsing the provided feed url", status_code=feed_data.status)
        return feed_data
