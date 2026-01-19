from django.urls import path

from .views import SignUpAPIView, VerifyEmailAPIView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="users-signup"),
    path(
        "verify-email/",
        VerifyEmailAPIView.as_view(),
        name="users-verify-email",
    ),
]
