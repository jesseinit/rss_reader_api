import json

import pytest
from django import http
from faker import Faker
from rest_framework import status


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, client, registered_user):
        """
        Test for a succesfull user login
        """
        payload = {"username": registered_user.username, "password": "K1#EzbuXsFWZ"}

        response = client.post("/api/v1/auth/login", payload)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["data"]["user"] == registered_user.id
        assert "refresh" in response_data["data"]["token"].keys()
        assert "access" in response_data["data"]["token"].keys()

    def test_login_with_bad_inputs(self, client, registered_user):
        """
        Test for errors when a user attempts to login with unprocessible inputs
        """
        input_payload = {"username": "", "password": "K1#EzbuXsFWZ"}
        expected_response = {
            "error": {
                "username": ["This field may not be blank."],
            }
        }
        response = client.post("/api/v1/auth/login", input_payload)
        response_data = response.json()
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data == expected_response

    def test_signup_with_wrong_credentials(self, client, registered_user):
        """
        Test for errors when a user attempts to login with wrong credentials
        """
        input_payload = {"username": registered_user.username, "password": "bigmanthing"}
        expected_response = {"message": "Your login credentials are not correct"}
        response = client.post("/api/v1/auth/login", input_payload)
        response_data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data == expected_response
