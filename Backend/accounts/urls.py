from django.urls import path
from accounts.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/search/", UserSearchView.as_view(), name="user_search"),
    path("request-password-reset/", RequestPasswordResetView.as_view(), name="request_password_reset"),
    path("verify-otp-reset-password/", VerifyOTPAndResetPasswordView.as_view(), name="verify_otp_reset_password"),
]
