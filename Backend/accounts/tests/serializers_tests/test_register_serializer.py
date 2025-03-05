import uuid
import pytest
from hypothesis import given, strategies as st, settings
from accounts.serializers import RegisterSerializer


@pytest.mark.django_db
@settings(deadline=None)
@given(
    first_name=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    ),
    last_name=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    ),
)
def test_register_serializer_positive(first_name, last_name):
    """
    Positive test: Valid registration with all required fields.
    """
    data = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "testpass123",
        "first_name": first_name,
        "last_name": last_name,
        "user_type": "student",
    }
    serializer = RegisterSerializer(data=data)
    assert (
        serializer.is_valid()
    ), f"Serializer should be valid. Errors: {serializer.errors}"
    user = serializer.save()
    assert user.email == data["email"]
    assert user.check_password("testpass123"), "Password should be set correctly."
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.user_type == "student"


@pytest.mark.django_db
def test_register_serializer_negative_missing_password():
    """
    Negative test: Missing password should make the serializer invalid.
    """
    data = {
        "email": f"{uuid.uuid4()}@example.com",
        "first_name": "NoPassword",
        "last_name": "User",
        "user_type": "teacher",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid(), "Serializer should be invalid without a password."
    assert "password" in serializer.errors, "Expected an error for missing 'password'."


@pytest.mark.django_db
@settings(deadline=None)
@given(long_name=st.text(min_size=256, max_size=256))
def test_register_serializer_edge_case_long_name(long_name):
    """
    Edge case test: Attempting to register a user with an excessively long first_name
    or last_name should fail at the serializer level.
    """
    data = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "testpass123",
        "first_name": long_name,
        "last_name": "TestLast",
        "user_type": "student",
    }
    serializer = RegisterSerializer(data=data)

    assert (
        not serializer.is_valid()
    ), "Serializer should be invalid for overly long first_name."
    assert "first_name" in serializer.errors, "Expected error message for first_name."
