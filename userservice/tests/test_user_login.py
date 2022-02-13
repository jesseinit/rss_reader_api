import pytest
from rest_framework import status


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, client, user_one):
        """
        Test for a succesfull user login
        """
        payload = {"username": user_one.username, "password": "K1#EzbuXsFWZ"}

        response = client.post("/api/v1/auth/login", payload)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["data"]["user"] == user_one.id
        assert "refresh" in response_data["data"]["token"].keys()
        assert "access" in response_data["data"]["token"].keys()

    def test_login_with_bad_inputs(self, client, user_one):
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

    def test_signup_with_wrong_credentials(self, client, user_one):
        """
        Test for errors when a user attempts to login with wrong credentials
        """
        input_payload = {"username": user_one.username, "password": "bigmanthing"}
        expected_response = {"message": "Your login credentials are not correct"}
        response = client.post("/api/v1/auth/login", input_payload)
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data == expected_response
