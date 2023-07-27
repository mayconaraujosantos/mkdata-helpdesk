from django.contrib.auth import models as auth_models
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from . import models


class SerializerBase(serializers.HyperlinkedModelSerializer):
    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.insert(0, "id")
        return fields


class UserAuthSerializer(SerializerBase):
    class Meta:
        model = models.User
        fields = ["id", "username", "name", "is_superuser", "url"]


class UserSerializer(SerializerBase):
    class Meta:
        model = models.User
        fields = "__all__"

    def create(self, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)


class GroupSerializer(SerializerBase):
    class Meta:
        model = auth_models.Group
        fields = "__all__"


class PermissionSerializer(SerializerBase):
    granted = serializers.BooleanField(read_only=True)

    class Meta:
        model = auth_models.Permission
        fields = "__all__"


class ContentTypeSerializer(SerializerBase):
    class Meta:
        model = auth_models.ContentType
        fields = "__all__"
