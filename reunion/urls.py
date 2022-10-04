from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Social Media API's",
        default_version="v1",
        description="Find all APIs below",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # swagger ui
    path(
        "swagger-ui/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("api/", include("social_app.urls")),
]
