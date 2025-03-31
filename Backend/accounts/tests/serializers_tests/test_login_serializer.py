import uuid
import pytest
from hypothesis import given, strategies as st, settings
from django.contrib.auth import get_user_model, authenticate
from accounts.serializers import LoginSerializer

User = get_user_model()


@pytest.mark.django_db
def test_login_serializer_positive():
    """
    Positive test: A user with valid credentials should receive tokens and user data.
    """
    email = f"{uuid.uuid4()}@example.com"
    password = "validpass123"

    # Create and authenticate user
    User.objects.create_user(
        email=email, password=password, first_name="Test", last_name="User"
    )

    data = {"email": email, "password": password}
    serializer = LoginSerializer(data=data)
    assert (
        serializer.is_valid()
    ), f"Serializer should be valid. Errors: {serializer.errors}"
    result = (
        serializer.validated_data
    ) 

    # Check result for expected fields
    assert "access" in result, "Expected access token in response."
    assert "refresh" in result, "Expected refresh token in response."
    assert "user" in result, "Expected user data in response."
    assert result["user"]["email"] == email, "Returned user email does not match."


@pytest.mark.django_db
def test_login_serializer_negative_wrong_credentials():
    """
    Negative test: Invalid credentials should fail validation.
    """
    # Create a user
    email = f"{uuid.uuid4()}@example.com"
    password = "correctpassword"
    User.objects.create_user(
        email=email, password=password, first_name="Test", last_name="User"
    )

    # Provide wrong password
    data = {"email": email, "password": "wrongpassword"}
    serializer = LoginSerializer(data=data)
    assert (
        not serializer.is_valid()
    ), "Serializer should be invalid for wrong credentials."
    assert "non_field_errors" in serializer.errors or "Invalid credentials" in str(
        serializer.errors
    ), "Expected 'Invalid credentials' error."


@pytest.mark.django_db
def test_login_serializer_edge_case_user_does_not_exist():
    """
    Edge case: Attempting to login with an email that doesn't exist in the database.
    """
    data = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "somepassword",
    }
    serializer = LoginSerializer(data=data)
    assert (
        not serializer.is_valid()
    ), "Serializer should be invalid if user does not exist."
    assert "Invalid credentials" in str(
        serializer.errors
    ), "Expected 'Invalid credentials' error."
