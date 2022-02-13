from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager Class for User Model"""

    def create_user(self, username: str = None, password: str = None, email: str = None):
        """Creates user instance"""
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    """User Model"""

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, default=None, null=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self) -> str:
        return f"<User {self.username}>"
