from django.urls import path

from .views import (
    LoginAPIView,
    SignUpAPIView,
    UserInfoAPIView,
    UserUpdateAPIView,
    VerifyEmailAPIView,
)

urlpatterns = [
    path("auth/register/", SignUpAPIView.as_view(), name="register"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/me/", UserInfoAPIView.as_view(), name="info"),
    path(
        "auth/verify-email/",
        VerifyEmailAPIView.as_view(),
        name="verify-email",
    ),
    path("users/me/", UserUpdateAPIView.as_view(), name="update"),
]
