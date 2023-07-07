from rest_framework import serializers


class UserChangePasswordParamsSerializer(serializers.Serializer):
    password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=True)
    reset = serializers.BooleanField(required=True)
