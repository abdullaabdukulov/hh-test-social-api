from common.utils.custom_response_decorator import custom_response
from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import EmailVerificationToken
from users.response_schema import (
    LOGIN_SCHEMA_RESPONSE,
    SIGNUP_SCHEMA_RESPONSE,
    USER_ME_SCHEMA_RESPONSE,
    USER_UPDATE_SCHEMA_RESPONSE,
    VERIFY_EMAIL_SCHEMA_RESPONSE,
)
from users.serializers import (
    LoginSerializer,
    SignUpSerializer,
    UserInfoSerializer,
    VerifyEmailSerializer,
)

User = get_user_model()


@custom_response
class SignUpAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses=SIGNUP_SCHEMA_RESPONSE)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, _token_obj = self.perform_create(serializer)

        return Response(
            {
                "message": (
                    "User created successfully. Please check your email "
                    "to verify it."
                ),
                "email": user.email,
                "full_name": user.full_name,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        return User.objects.register_user(**serializer.validated_data)


@custom_response
class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses=VERIFY_EMAIL_SCHEMA_RESPONSE)
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        token_obj = EmailVerificationToken.objects.select_related("user").get(
            token=token
        )

        user = token_obj.user
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        token_obj.used_at = timezone.now()
        token_obj.save(update_fields=["used_at"])

        return Response(
            {
                "message": "Email verified successfully.",
                "email": user.email,
                "full_name": user.full_name,
                "username": user.username,
            }
        )


@custom_response
class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses=LOGIN_SCHEMA_RESPONSE)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class UserInfoAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(responses=USER_ME_SCHEMA_RESPONSE)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserInfoSerializer
    http_method_names = ["patch"]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(responses=USER_UPDATE_SCHEMA_RESPONSE)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
