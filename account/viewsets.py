import logging
from typing import Any, Optional

from django.contrib.auth import models as auth_models
from drf_yasg.utils import status, swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from account import exceptions, filters, models, params_serializer, queries, serializers

logger = logging.getLogger(__name__)


class AuthViewSetBase(viewsets.ModelViewSet):
    """
    Base class for authentication view sets.

    This class provides common functionality for authentication-related
    view sets. It extends the ModelViewSet from the Django Rest Framework and
    adds additional authentication-specific features.
    """

    _permission: Optional[str] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._permission = self.get_permission_name()

    def get_permission_name(self):
        if self.serializer_class:
            meta = self.serializer_class.Meta.model._meta
            return f"{meta.app_label}.view_{meta.model_name}".lower()
        return ""

    def check_permissions(self, request, *args, **kwargs):
        if request.user.has_perm(self._permission):
            return self.list(request, *args, **kwargs)
        raise exceptions.PermissionNotAllowedException

    @swagger_auto_schema(
        operation_description="Retrieve all",
        responses={status.HTTP_200_OK: "success"},
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Any:
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve all",
        responses={status.HTTP_200_OK: "success"},
    )
    def retrieve(self, request, *args: Any, **kwargs: Any) -> Any:
        return super().retrieve(request, *args, **kwargs)


class UserViewSet(AuthViewSetBase):
    queryset = models.User.objects.all().exclude(is_default=True)
    serializer_class = serializers.UserSerializer
    filter_class = filters.UserFilter
    ordering_fields = "__all__"
    ordering = ("name",)

    @action(detail=True, methods=["PATCH"])
    def change_password(self, request, *args, **kwargs):
        serializer = params_serializer.UserChangePasswordParamsSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        reset_password = serializer.data.get("reset", False)
        password = serializer.data.get("password", None)
        new_password = serializer.data.get("new_password")

        if not reset_password and not user.check_password(raw_password=password):
            raise exceptions.InvalidPasswordException

        user.set_password(raw_password=new_password)
        user.save()
        return Response(data={"detail": True})


class GroupViewSet(AuthViewSetBase):
    queryset = auth_models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    filter_class = filters.GroupFilter
    ordering_fields = "__all__"
    ordering = ("name",)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Any:
        if "user" in request.query_params:
            self.queryset = queries.get_user_group(
                user_id=request.query_params.get("user")
            )
        return super(GroupViewSet, self).list(request, *args, **kwargs)


class PermissionViewSet(AuthViewSetBase):
    queryset = auth_models.Permission.objects.all()
    serializer_class = serializers.PermissionSerializer
    filter_class = filters.PermissionFilter
    ordering_fields = "__all__"
    ordering = "content_type"


class ContentTypeViewSet(AuthViewSetBase):
    queryset = auth_models.ContentType.objects.all()
    serializer_class = serializers.ContentTypeSerializer
    filter_class = filters.ContenTypeFilter
    ordering_fields = "__all__"
    ordering = ("app_label",)
