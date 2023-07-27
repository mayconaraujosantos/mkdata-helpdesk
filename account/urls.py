from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from account import viewsets

router = routers.DefaultRouter()
router.register(r"user", viewsets.UserViewSet)
router.register(r"group", viewsets.GroupViewSet)
router.register(r"permission", viewsets.PermissionViewSet)
router.register(r"content_type", viewsets.ContentTypeViewSet)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns += router.urls
