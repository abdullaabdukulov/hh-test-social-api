"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.settings import (
    base as settings,
    django_settings_module,
)


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = (
            ["http"] if django_settings_module == "development" else ["https"]
        )
        return schema


schema_view = get_schema_view(
    openapi.Info(
        "Social API",
        "v1.0",
        'Project name: "Social API"',
        contact=openapi.Contact(
            name="abdulla.abdukulov.uz",
            url="https://abdulla.abdukulov.uz",
        ),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

urlpatterns = [path("default-admin-panel/", admin.site.urls)]

urlpatterns += [
    path("api/v1/", include(("users.urls", "users"), "users")),
    path("api/v1/", include(("posts.urls", "posts"), namespace="posts")),
    path(
        "api/v1/", include(("comments.urls", "comments"), namespace="comments")
    ),
    path("api/v1/", include(("likes.urls", "likes"), namespace="likes")),
]
if django_settings_module in ("development", "staging"):
    urlpatterns += [
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

if django_settings_module == "development":
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
