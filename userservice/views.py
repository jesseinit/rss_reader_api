import utils.helpers as helpers
from rest_framework import status, viewsets
from rest_framework.decorators import action

import userservice.serializers as serializers
import userservice.services as services


class UserOnboardingViewset(viewsets.ViewSet):
    """Handles User Onboarding Processes"""

    permission_classes = ()
    authentication_classes = ()

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
