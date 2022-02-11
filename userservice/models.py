from typing import Type

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager Class for User Model"""

    def create_user(self, username: str = None, password: str = None):
        """Creates user instance"""
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user


class UserQuerysetManager(models.QuerySet):
    """Custom Queryset Class for User Model"""

    def is_existing(self, username: str = None) -> bool:
        """Checks if a user exists"""
        return self.filter(username=username).exists()


class User(AbstractBaseUser):
    """User Model"""

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    USERNAME_FIELD = "username"

    objects = UserManager.from_queryset(UserQuerysetManager)()
