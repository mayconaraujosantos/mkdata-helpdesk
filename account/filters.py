from django.contrib.auth import models as auth_models
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


class GroupFilter(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr=choices.LIKE)

    class Meta:
        model = auth_models.Group
        fields = ["name"]


class PermissionFilter(filterset.FilterSet):
    codename = filterset.CharFilter(lookup_expr=choices.LIKE)
    name = filterset.CharFilter(lookup_expr=choices.LIKE)
    codename_or_name = filterset.CharFilter(method="filter_codename_name")
    content_type = filterset.NumberFilter(lookup_expr=choices.EXACT)

    @staticmethod
    def filter_codename_name(queryset, name, value):
        return queryset.filter(
            Q(codename__unaccent__icontains=value) | Q(name__unaccent__icontains=value)
        )

    class Meta:
        model = auth_models.Permission
        fields = ["codename", "name", "codename_or_name", "content_type"]


class ContenTypeFilter(filterset.FilterSet):
    app_label = filterset.CharFilter(lookup_expr=choices.LIKE)
    model = filterset.CharFilter(lookup_expr=choices.LIKE)
    app_label_or_model = filterset.CharFilter(method="filter_app_label_model")

    @staticmethod
    def filter_app_label_model(queryset, name, value):
        return queryset.filter(
            Q(app_label__unaccent__icontains=value)
            | Q(model__unaccent__icontains=value)
        )

    class Meta:
        model = auth_models.ContentType
        fields = ["app_label", "model", "app_label_or_model"]
