import uuid
import pytest
import pyotp
from hypothesis import given, strategies as st, settings
from accounts.models import CustomUser
from accounts.serializers import VerifyOTPSerializer


@pytest.mark.django_db
@settings(deadline=None)
@given(
    new_password=st.text(
        min_size=6,
        max_size=12,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_verify_otp_serializer_positive(new_password):
    """
    Positive test: Provide a valid email, correct OTP, and a valid new_password.
    Should result in a successful password reset.
    """
    # Create a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="oldPassword123",
        user_type="student",
    )
    # Generate a valid TOTP
    totp = pyotp.TOTP(user.otp_secret, interval=60)
    valid_otp = totp.now()

    data = {
        "email": user.email,
        "otp": valid_otp,
        "new_password": new_password,
    }
    serializer = VerifyOTPSerializer(data=data)

    if serializer.is_valid():
        validated_data = serializer.validated_data
        assert (
            validated_data["message"] == "Password reset successful."
        ), "Expected success message from serializer."
        
    user.refresh_from_db()
    assert user.check_password(new_password), "New password should be set correctly."


@pytest.mark.django_db
def test_verify_otp_serializer_negative_invalid_otp():
    """
    Negative test: Provide an incorrect OTP, expecting validation error.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="someOldPass", user_type="teacher"
    )
    # Generate a valid TOTP but modify it to ensure it's incorrect
    totp = pyotp.TOTP(user.otp_secret, interval=60)
    invalid_otp = str(int(totp.now()) + 1)  # Just shift the valid code slightly

    data = {
        "email": user.email,
        "otp": invalid_otp,
        "new_password": "SomeNewPass123",
    }
    serializer = VerifyOTPSerializer(data=data)
    assert (
        not serializer.is_valid()
    ), "Serializer should be invalid with an incorrect OTP."
    assert "Invalid OTP." in str(
        serializer.errors
    ), "Expected 'Invalid OTP.' error message."


@pytest.mark.django_db
def test_verify_otp_serializer_edge_case_short_password():
    """
    Edge case: The new_password is fewer than 6 characters, violating the min_length constraint.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="someOldPass", user_type="student"
    )
    totp = pyotp.TOTP(user.otp_secret, interval=60)
    valid_otp = totp.now()

    data = {
        "email": user.email,
        "otp": valid_otp,
        "new_password": "123",  # Too short (min_length=6)
    }
    serializer = VerifyOTPSerializer(data=data)
    assert (
        not serializer.is_valid()
    ), "Serializer should be invalid for a short new_password."
    assert (
        "new_password" in serializer.errors
    ), "Expected an error on 'new_password' field."
