from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from dj_rest_auth.registration.views import RegisterView
from accounts.serializers import CustomRegisterSerializer


schema_view = get_schema_view(
    openapi.Info(
        title="eLearning API",
        default_version="v1",
        description="API documentation for the eLearning application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


RegisterView.serializer_class = CustomRegisterSerializer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", LoginView.as_view(), name="rest_login"),
    path("api/auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("api/auth/register/", RegisterView.as_view(), name="rest_register"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
    # API Documentation Endpoints
    path(
        "apidocs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"
    ),
    path("redocs/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-docs"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
