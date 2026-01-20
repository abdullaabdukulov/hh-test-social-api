from common.response_schema import ERRORS_SCHEMA
from drf_yasg import openapi
from rest_framework import status

FEED_POST_ITEM = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid"),
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "content": openapi.Schema(type=openapi.TYPE_STRING),
        "likes": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING, format="uuid"),
        ),
    },
)

FEED_USER_ITEM = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(type=openapi.TYPE_STRING),
        "posts": openapi.Schema(type=openapi.TYPE_ARRAY, items=FEED_POST_ITEM),
    },
)

PAGINATED_FEED = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
        "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "previous": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "results": openapi.Schema(
            type=openapi.TYPE_ARRAY, items=FEED_USER_ITEM
        ),
    },
)

FEED_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="Feed",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": PAGINATED_FEED,
        },
    )
}

POST_LIST_ITEM = openapi.Schema(
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

POST_DETAIL_ITEM = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid"),
        "author": openapi.Schema(type=openapi.TYPE_STRING),
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "content": openapi.Schema(type=openapi.TYPE_STRING),
        "likes": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING, format="uuid"),
        ),
        "comments": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_OBJECT),
        ),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time"
        ),
        "updated_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time"
        ),
    },
)

PAGINATED_POSTS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
        "next": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "previous": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "results": openapi.Schema(
            type=openapi.TYPE_ARRAY, items=POST_LIST_ITEM
        ),
    },
)

POSTS_LIST_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="PostsList",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": PAGINATED_POSTS,
        },
    )
}

POST_DETAIL_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="PostDetail",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": ERRORS_SCHEMA,
            "data": POST_DETAIL_ITEM,
        },
    )
}
