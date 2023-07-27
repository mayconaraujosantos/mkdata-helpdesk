from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, reverse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from helpdesk import settings

SchemaView = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

routers = DefaultRouter()

urlpatterns = [
    path(
        "swagger<format>/",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        SchemaView.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("admin/", admin.site.urls),
    path("", lambda request: redirect(reverse("api-root"))),
    path("api/v1/", include(routers.urls), name="api-root"),
]


if "account.apps.AccountConfig" in settings.INSTALLED_APPS:
    urlpatterns.append(path("api/auth/", include("account.urls")))
