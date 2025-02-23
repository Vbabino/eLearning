from django.urls import path
from accounts.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User Management
    path("user/search/", UserSearchView.as_view(), name="user_search"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path(
        "user/upload-profile-photo/<int:pk>/",
        UploadProfilePhotoView.as_view(),
        name="upload_profile_photo",
    ),
    path("user-photo/<int:pk>/", GetProfilePhotoView.as_view(), name="user_photo"),
    # Password Reset
    path(
        "request-password-reset/",
        RequestPasswordResetView.as_view(),
        name="request_password_reset",
    ),
    path(
        "verify-otp-reset-password/",
        VerifyOTPAndResetPasswordView.as_view(),
        name="verify_otp_reset_password",
    ),
]
