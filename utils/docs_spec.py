from drf_yasg import openapi

ONBOARDING_REGISTER_RESPONSES = {
    200: openapi.Response(
        description="Registration Success",
        examples={"application/json": {"data": {"id": 7, "email": "mee1@go.com", "username": "men_them1"}}},
    ),
    422: openapi.Response(
        description="Bad User Input",
        examples={
            "application/json": {
                "error": {
                    "username": ["This field may not be blank."],
                    "password": ["This field may not be blank."],
                    "email": ["This field may not be blank."],
                }
            }
        },
    ),
}

ONBOARDING_LOGIN_RESPONSES = {
    200: openapi.Response(
        description="Login Success",
        examples={
            "application/json": {
                "data": {
                    "user": 1,
                    "token": {
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    },
                }
            }
        },
    ),
    400: openapi.Response(
        description="Invalid Login Credentails",
        examples={"application/json": {"message": "Your login credentials are not correct"}},
    ),
    422: openapi.Response(
        description="Bad User Input",
        examples={
            "application/json": {
                "error": {
                    "username": ["This field may not be blank."],
                    "password": ["This field may not be blank."],
                }
            }
        },
    ),
}
