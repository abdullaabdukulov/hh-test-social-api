from common.response_schema import ERRORS_SCHEMA
from drf_yasg import openapi
from rest_framework import status

COMMENT_ITEM = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid"),
        "author": openapi.Schema(type=openapi.TYPE_STRING),
        "content": openapi.Schema(type=openapi.TYPE_STRING),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time"
        ),
    },
)

COMMENTS_LIST_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="CommentsList",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": openapi.Schema(
                type=openapi.TYPE_ARRAY, items=COMMENT_ITEM
            ),
        },
    )
}

COMMENT_CREATE_SCHEMA_RESPONSE = {
    status.HTTP_201_CREATED: openapi.Schema(
        title="CommentCreate",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": COMMENT_ITEM,
        },
    )
}

COMMENT_DELETE_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="CommentDelete",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        },
    )
}
