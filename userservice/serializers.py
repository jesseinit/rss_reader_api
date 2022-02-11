from rest_framework import serializers

from userservice.models import User


class FieldValidators:
    @staticmethod
    def validate_existing_username(username: str) -> None:
        """
        Checks for existing username
        """
        if User.objects.is_existing(username=username) is True:
            raise serializers.ValidationError("A user with this username exists")


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[FieldValidators.validate_existing_username])
    password = serializers.CharField(min_length=6, max_length=16)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=6, max_length=16)
