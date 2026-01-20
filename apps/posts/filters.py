from django_filters import rest_framework as filters

from .models import Post


class PostFilter(filters.FilterSet):
    date_from = filters.IsoDateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    date_to = filters.IsoDateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = Post
        fields = ("date_from", "date_to")
