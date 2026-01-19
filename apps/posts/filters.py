import django_filters
from django_filters import rest_framework as filters

from .models import Post


class PostFilter(filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Post
        fields = ("created_at",)
