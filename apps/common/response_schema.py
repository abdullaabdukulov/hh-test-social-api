from drf_yasg import openapi

ERRORS_SCHEMA = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_OBJECT),
)
