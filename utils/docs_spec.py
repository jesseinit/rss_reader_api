from drf_yasg import openapi

PAGE_SIZE_PARAMS = openapi.Parameter(
    "page_size",
    in_=openapi.IN_QUERY,
    description="Defines how many records you want per page.",
    type=openapi.TYPE_INTEGER,
)

PAGE_PARAMS = openapi.Parameter(
    "page",
    in_=openapi.IN_QUERY,
    description="Defines what page number you want to navigate to.",
    type=openapi.TYPE_INTEGER,
)

FEED_ID_PARAMS = openapi.Parameter(
    "feed_id",
    in_=openapi.IN_QUERY,
    description="Feed ID",
    type=openapi.TYPE_INTEGER,
)

READ_UNREAD_STATUS_PARAMS = openapi.Parameter(
    "status",
    in_=openapi.IN_QUERY,
    description="Read or Unread Status",
    type=openapi.TYPE_STRING,
    enum=["read", "unread"],
    default="read",
    required=True,
)

PAGINATED__OK_RESPONSE = openapi.Response(
    description="Results",
    examples={"application/json": {"count": 2, "total_pages": 1, "next": None, "previous": None, "data": ["..."]}},
)

UNAUTHENTICATED_RESPONSE = {
    401: openapi.Response(
        description="Authentication Failed",
        examples={"application/json": {"detail": "Authentication credentials were not provided."}},
    )
}


ONBOARDING_REGISTER_RESPONSES = {
    201: openapi.Response(
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
    **UNAUTHENTICATED_RESPONSE,
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
    **UNAUTHENTICATED_RESPONSE,
}


FEED_ADD_URL_RESPONSES = {
    201: openapi.Response(
        description="Feed URL Add Success",
        examples={
            "application/json": {
                "data": {
                    "id": 6,
                    "title": "Tweakers Mixed RSS Feed",
                    "url": "https://feeds.feedburner.com/tweakers/mixed",
                    "created_at": "2022-02-13T22:18:31.143167Z",
                    "updated_at": "2022-02-13T22:17:00Z",
                    "registered_by": 1,
                    "followers": [1],
                }
            }
        },
    ),
    422: openapi.Response(
        description="Bad User Input",
        examples={"application/json": {"error": {"url": ["This field may not be blank."]}}},
    ),
    **UNAUTHENTICATED_RESPONSE,
}

REGISTERED_FEEDS_RESPONSE = {
    200: PAGINATED__OK_RESPONSE,
    **UNAUTHENTICATED_RESPONSE,
}

FEEDS_ITEMS_RESPONSE = {
    200: PAGINATED__OK_RESPONSE,
    **UNAUTHENTICATED_RESPONSE,
    400: openapi.Response(
        description="Bad User Input",
        examples={"application/json": {"message": "Feed item not found"}},
    ),
}

READ_UNREAD_ITEMS_RESPONSE = {
    200: PAGINATED__OK_RESPONSE,
    422: openapi.Response(
        description="Bad User Input",
        examples={"application/json": {"error": {"status": ["This field is required."]}}},
    ),
    400: openapi.Response(
        description="Bad User Input",
        examples={"application/json": {"message": "Feed not found"}},
    ),
    **UNAUTHENTICATED_RESPONSE,
}

MARK_READ_UNREAD_FEED_ITEMS_RESPONSE = {
    200: openapi.Response(
        description="Success",
        examples={"application/json": {"data": {"id": 7, "is_read": False, "user": 1, "feed_item": 350, "feed": 5}}},
    ),
    **UNAUTHENTICATED_RESPONSE,
    400: openapi.Response(
        description="Bad User Input",
        examples={"application/json": {"message": "Feed item not found"}},
    ),
}

FOLLOW_UNFOLLOW_FEED_RESPONSE = {
    200: openapi.Response(
        description="Success",
        examples={"application/json": {"data": {"message": "Followed 1 feed(s)"}}},
    ),
    400: openapi.Response(
        description="Bad User Input",
        examples={"application/json": {"message": "Feeds not found"}},
    ),
    **UNAUTHENTICATED_RESPONSE,
}

FORCE_UPDATE_RESPONSE = {
    200: openapi.Response(
        description="Success",
        examples={
            "application/json": {"data": "Feed update has been triggered triggered. Timeline would be updated shortly"}
        },
    ),
    400: openapi.Response(
        description="Bad User Input",
        examples={"application/json": {"message": "Feed not found"}},
    ),
    **UNAUTHENTICATED_RESPONSE,
}
