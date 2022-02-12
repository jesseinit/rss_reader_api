from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from userservice.models import User


class FieldValidators:
    @staticmethod
    def validate_existing_username(username: str) -> None:
        """
        Checks for existing username
        """
        if User.objects.filter(username=username).exists() is True:
            raise serializers.ValidationError("A user with this username exists")

    @staticmethod
    def validate_existing_email(email: str) -> None:
        """
        Checks for existing email
        """
        if User.objects.filter(email=email).exists() is True:
            raise serializers.ValidationError("A user with this email exists")


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[FieldValidators.validate_existing_username])
    password = serializers.CharField(min_length=6, max_length=16)
    email = serializers.CharField(validators=[FieldValidators.validate_existing_email])


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=6, max_length=16)
