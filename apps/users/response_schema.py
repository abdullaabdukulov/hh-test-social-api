from common.response_schema import ERRORS_SCHEMA
from drf_yasg import openapi
from rest_framework import status

SIGNUP_SCHEMA_RESPONSE = {
    status.HTTP_201_CREATED: openapi.Schema(
        title="SignUp",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "full_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "username": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
}

VERIFY_EMAIL_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="VerifyEmail",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "full_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "username": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    ),
}

LOGIN_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="Login",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Schema(type=openapi.TYPE_STRING),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
}

USER_INFO_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, format="email"),
        "username": openapi.Schema(type=openapi.TYPE_STRING),
        "full_name": openapi.Schema(type=openapi.TYPE_STRING),
        "is_verified": openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)

USER_ME_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="UserMe",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": USER_INFO_SCHEMA,
        },
    )
}

USER_UPDATE_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="UserUpdate",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": USER_INFO_SCHEMA,
        },
    )
}
