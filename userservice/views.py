import utils.docs_spec as schema_spec
import utils.helpers as helpers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

import userservice.serializers as serializers
import userservice.services as services


class UserOnboardingViewset(viewsets.ViewSet):
    """Handles User Onboarding Processes"""

    permission_classes = ()
    authentication_classes = ()

    @swagger_auto_schema(
        operation_summary="Register A User",
        tags=["Onboarding"],
        request_body=serializers.RegisterSerializer,
        responses=schema_spec.ONBOARDING_REGISTER_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="register")
    def register_user(self, request):
        """Register A User"""

        serialized_data = serializers.RegisterSerializer(data=request.data)
        if not serialized_data.is_valid():
            return helpers.ResponseManager.handle_response(
                error=serialized_data.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        service_response = services.OnboardingService.register(**serialized_data.data)
        return helpers.ResponseManager.handle_response(data=service_response, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Login A User",
        tags=["Onboarding"],
        request_body=serializers.LoginSerializer,
        responses=schema_spec.ONBOARDING_LOGIN_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="login")
    def login_user(self, request):
        """Login A User"""

        serialized_data = serializers.LoginSerializer(data=request.data)
        if not serialized_data.is_valid():
            return helpers.ResponseManager.handle_response(
                error=serialized_data.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        service_response = services.OnboardingService.login(**serialized_data.data)
        return helpers.ResponseManager.handle_response(data=service_response, status=status.HTTP_200_OK)
