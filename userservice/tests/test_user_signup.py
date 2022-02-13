import json

import pytest
from django import http
from faker import Faker
from rest_framework import status


@pytest.mark.django_db
class TestRegistration:
    def test_signup_success(self, client):
        """
        Test for a succesfull user signup
        """
        payload = {"username": "some-username", "password": "bigmanthing", "email": "mee@go.com"}
        response = client.post("/api/v1/auth/register", payload)
        res = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert res["data"]["username"] == payload["username"]
        assert res["data"]["email"] == payload["email"]

    def test_signup_with_bad_inputs(self, client):
        """
        Test for errors when a user attempts to signup with unprocessible inputs
        """
        input_payload = {}
        expected_response = {
            "error": {
                "username": ["This field is required."],
                "password": ["This field is required."],
                "email": ["This field is required."],
            }
        }
        response = client.post("/api/v1/auth/register", input_payload)
        response_data = response.json()
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data == expected_response

    def test_signup_with_exisiting_inputs(self, client, user_one):
        """
        Test for errors when a user attempts to signup with existing inputs
        """
        input_payload = {"username": "jesseinit", "password": "bigmanthing", "email": "john.doe@mail.com"}
        expected_response = {
            "error": {
                "email": ["A user with this email exists"],
                "username": ["A user with this username exists"],
            }
        }
        response = client.post("/api/v1/auth/register", input_payload)
        response_data = response.json()
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data == expected_response
