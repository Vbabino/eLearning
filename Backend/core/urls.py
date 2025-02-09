from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView

schema_view = get_schema_view(
    openapi.Info(
        title="eLearning API",
        default_version="v1",
        description="API documentation for the eLearning application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("register/", RegisterView.as_view(), name="rest_register"),

    # API Documentation Endpoints
    path(
        "apidocs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"
    ),
    path("redocs/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-docs"),
]
