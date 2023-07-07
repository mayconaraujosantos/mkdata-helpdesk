import logging
from typing import Any

from drf_yasg.utils import status, swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from account import exceptions, filters, models, params_serializer, serializers

logger = logging.getLogger(__name__)


class AuthViewSetBase(viewsets.ModelViewSet):
    """
    Base class for authentication view sets.

    This class provides common functionality for authentication-related view sets.
    It extends the ModelViewSet from the Django Rest Framework and adds additional
    authentication-specific features.
    """

    _permission: str = None

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
        rs = params_serializer.UserChangePasswordParamsSerializer(data=request.data)
        rs.is_valid(raise_exception=True)

        user = self.get_object()
        if not rs.data.get("reset") and not user.check_password(
            raw_password=rs.data.get("password", None)
        ):
            raise exceptions.InvalidPasswordException

        user.set_password(raw_password=rs.data.get("new_password"))
        user.save()
        return Response(data={"message": "Password changed successfully"})
