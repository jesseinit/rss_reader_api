from pytest_factoryboy import register

from userservice.tests.factories import UserFactory

register(UserFactory, "registered_user", username="jesseinit", email="john.doe@mail.com")
