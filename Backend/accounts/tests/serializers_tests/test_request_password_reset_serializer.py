import uuid
import pytest
from hypothesis import given, strategies as st, settings
from accounts.models import CustomUser
from accounts.serializers import RequestPasswordResetSerializer

@pytest.mark.django_db
def test_request_password_reset_serializer_positive():
    """
    Positive test: A user with an existing email should pass serializer validation
    and trigger OTP sending.
    """
    email = f"{uuid.uuid4()}@example.com"
    CustomUser.objects.create_user(
        email=email,
        password="testPassword123",
        user_type="student",
    )

    data = {"email": email}
    serializer = RequestPasswordResetSerializer(data=data)
    assert serializer.is_valid(), f"Serializer should be valid. Errors: {serializer.errors}"

    # Call save() and ensure it returns the correct message
    result = serializer.save()
    assert "message" in result, "Expected a 'message' field in serializer output."
    assert result["message"] == "OTP sent to email.", "Expected OTP sending confirmation."


@pytest.mark.django_db
def test_request_password_reset_serializer_negative_no_user():
    """
    Negative test: Serializer should fail for an email that does not exist in the database.
    """
    non_existent_email = f"{uuid.uuid4()}@example.com"
    data = {"email": non_existent_email}
    serializer = RequestPasswordResetSerializer(data=data)
    assert not serializer.is_valid(), "Serializer should be invalid for a non-existent email."
    assert "email" in serializer.errors, "Expected an error on the 'email' field."
    assert (
        "User with this email does not exist." in serializer.errors["email"]
    ), "Expected 'User with this email does not exist.' error message."


@pytest.mark.django_db
def test_request_password_reset_serializer_edge_case_long_email():
    """
    Edge case: A very long email (exceeding typical constraints) should
    either fail EmailField validation or pass if not restricted.
    """
    long_local_part = "a" * 256
    long_email = f"{long_local_part}@example.com"

    # Create a user with a long email to test DB constraints
    try:
        CustomUser.objects.create_user(
            email=long_email,
            password="testPass123",
            user_type="teacher",
        )
    except Exception as e:
        pytest.skip(f"Could not create user with long email due to DB constraint: {e}")

    data = {"email": long_email}
    serializer = RequestPasswordResetSerializer(data=data)
    is_valid = serializer.is_valid()

    if is_valid:
        # If it passes validation and DB constraints, ensure save() works
        result = serializer.save()
        assert "message" in result, "Expected a 'message' field in serializer output."
        assert result["message"] == "OTP sent to email.", "Expected OTP sending confirmation."
    else:
        # If system does not permit such long emails
        assert not is_valid, "Serializer should be invalid for an overly long email."
        assert "email" in serializer.errors, "Expected an error on the 'email' field."
