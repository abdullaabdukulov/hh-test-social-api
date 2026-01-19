from drf_yasg import openapi
from rest_framework import status

POST_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid"),
        "author": openapi.Schema(type=openapi.TYPE_STRING),
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "content": openapi.Schema(type=openapi.TYPE_STRING),
        "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time"
        ),
        "updated_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time"
        ),
    },
)

POSTS_LIST_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="PostsList",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT),
            ),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "next": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True
                    ),
                    "previous": openapi.Schema(
                        type=openapi.TYPE_STRING, nullable=True
                    ),
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY, items=POST_SCHEMA
                    ),
                },
            ),
        },
    )
}

POST_DETAIL_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="PostDetail",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT),
            ),
            "data": POST_SCHEMA,
        },
    )
}
