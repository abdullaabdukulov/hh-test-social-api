from common.response_schema import ERRORS_SCHEMA
from drf_yasg import openapi
from rest_framework import status

MESSAGE_DATA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
)

LIKE_ACTION_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="LikeAction",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": MESSAGE_DATA,
        },
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Schema(
        title="LikeBadRequest",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
        },
    ),
    status.HTTP_404_NOT_FOUND: openapi.Schema(
        title="LikeNotFound",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
        },
    ),
    status.HTTP_401_UNAUTHORIZED: openapi.Schema(
        title="LikeUnauthorized",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
        },
    ),
}
