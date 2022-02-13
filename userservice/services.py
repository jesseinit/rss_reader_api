from typing import Dict

from django.contrib.auth.hashers import check_password
from rest_framework import status
from utils.helpers import CustomAPIException, TokenManager

from userservice.models import User


class OnboardingService:
    def register(username: str = None, email: str = None, password: str = None) -> Dict:
        """Service method that handles creating a user account"""

        # Get or create user
        created_user = User.objects.create_user(username=username, password=password, email=email)

        return {
            "id": created_user.id,
            "email": created_user.email,
            "username": created_user.username,
        }

    def login(username: str = None, password: str = None) -> Dict:
        """Service method that handles login for a user"""

        user = User.objects.filter(username=username).first()

        if user is None:
            raise CustomAPIException(
                "Your login credentials are not correct",
                status.HTTP_400_BAD_REQUEST,
            )

        is_valid_password = check_password(password, user.password)
        if not is_valid_password:
            raise CustomAPIException(
                "Your login credentials are not correct",
                status.HTTP_400_BAD_REQUEST,
            )

        return TokenManager.prepare_user_token(user)
