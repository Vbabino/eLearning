import uuid
import pytest
import pyotp
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser

@pytest.mark.django_db
@settings(deadline=None)
@given(
    new_password=st.text(
        min_size=6,
        max_size=12,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
    )
)
def test_verify_otp_reset_password_view_positive(new_password):
    """
    Positive test: Provide a valid email, correct OTP, and a valid new_password.
    Expect a 200 response and 'Password reset successful.' message.
    """
    client = APIClient()
    url = reverse("verify_otp_reset_password")

    # Create a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="oldPassword123",
        user_type="student",
    )

    # Generate a valid TOTP code for this user
    totp = pyotp.TOTP(user.otp_secret, interval=60)
    valid_otp = totp.now()

    data = {
        "email": user.email,
        "otp": valid_otp,
        "new_password": new_password,
    }
    response = client.post(url, data=data, format="json")

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.json()}"
    )
    assert response.json().get("message") == "Password reset successful.", (
        "Expected 'Password reset successful.' message."
    )

    # Confirm the user's password actually changed
    user.refresh_from_db()
    assert user.check_password(new_password), "New password should be properly set."


@pytest.mark.django_db
def test_verify_otp_reset_password_view_negative_invalid_otp():
    """
    Negative test: Provide an invalid OTP, expecting a 400 response with 'Invalid OTP.' message.
    """
    client = APIClient()
    url = reverse("verify_otp_reset_password")

    # Create a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="someOldPass",
        user_type="teacher",
    )

    # Generate a correct OTP but modify it to ensure it's invalid
    totp = pyotp.TOTP(user.otp_secret, interval=60)
    invalid_otp = str(int(totp.now()) + 1)  # Slightly off from the valid code

    data = {
        "email": user.email,
        "otp": invalid_otp,
        "new_password": "MyNewPass123",
    }
    response = client.post(url, data=data, format="json")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.json()}"
    )
    assert "Invalid OTP." in str(response.json()), (
        "Expected 'Invalid OTP.' error message."
    )


@pytest.mark.django_db
def test_verify_otp_reset_password_view_edge_case_short_password():
    """
    Edge case: Provide a valid OTP but a new_password shorter than 6 chars.
    Expect a 400 response with a validation error on 'new_password'.
    """
    client = APIClient()
    url = reverse("verify_otp_reset_password")

    # Create a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="initialPass456",
        user_type="student",
    )

    # Generate a valid TOTP code
    totp = pyotp.TOTP(user.otp_secret, interval=60)
    valid_otp = totp.now()

    data = {
        "email": user.email,
        "otp": valid_otp,
        "new_password": "123",  # Too short (min_length=6)
    }
    response = client.post(url, data=data, format="json")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.json()}"
    )
    # Check the error references the new_password field
    assert "new_password" in response.json(), (
        "Expected validation error for 'new_password' due to insufficient length."
    )