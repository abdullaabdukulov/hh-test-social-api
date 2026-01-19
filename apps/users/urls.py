from django.urls import path

from .views import (
    LoginAPIView,
    SignUpAPIView,
    UserInfoAPIView,
    UserUpdateAPIView,
    VerifyEmailAPIView,
)

urlpatterns = [
    path("register/", SignUpAPIView.as_view(), name="register"),
    path(
        "verify-email/",
        VerifyEmailAPIView.as_view(),
        name="verify-email",
    ),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("me/", UserInfoAPIView.as_view(), name="info"),
    path("me/update/", UserUpdateAPIView.as_view(), name="update"),
]
