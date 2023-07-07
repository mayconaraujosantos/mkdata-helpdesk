from django.db.models import Q
from django_filters import filterset, widgets

from account import choices, models


class UserFilter(filterset.FilterSet):
    username = filterset.CharFilter(lookup_expr=choices.LIKE)
    name = filterset.CharFilter(lookup_expr=choices.LIKE)
    username_or_name = filterset.CharFilter(method="filter_username_name")
    is_active = filterset.BooleanFilter(widget=widgets.BooleanWidget())

    @staticmethod
    def filter_username_name(queryset, name, value):
        return queryset.filter(
            Q(username__unaccent__icontains=value) | Q(name__unaccent__icontains=value)
        )

    class Meta:
        model = models.User
        fields = ["username", "name", "username_or_name", "is_active"]
