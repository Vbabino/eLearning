import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
from accounts.serializers import LogoutSerializer

@pytest.mark.django_db
def test_logout_serializer_positive():
    """
    Positive test: Providing a valid refresh token should pass serialization.
    """
    # Create a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="validpass123",
        user_type="student",
    )
    # Generate a valid refresh token for this user
    refresh = RefreshToken.for_user(user)

    # Prepare serializer data
    data = {"refresh": str(refresh)}
    serializer = LogoutSerializer(data=data)
    assert serializer.is_valid(), f"Expected serializer to be valid. Errors: {serializer.errors}"


@pytest.mark.django_db
def test_logout_serializer_negative():
    """
    Negative test: Providing an invalid or malformed refresh token should fail validation.
    """
    data = {"refresh": "invalid.token.string"}
    serializer = LogoutSerializer(data=data)

    assert (
        not serializer.is_valid()
    ), "Expected serializer to be invalid with a malformed token."
    assert (
        "refresh" in serializer.errors
    ), "Expected error on 'refresh' field for invalid token."


@pytest.mark.django_db
@given(
    token_str=st.text(
        min_size=1,
        max_size=5,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_logout_serializer_edge_case_short_token(token_str):
    """
    Edge case test: A refresh token that's too short or doesn't match typical structure.
    """
    data = {"refresh": token_str}
    serializer = LogoutSerializer(data=data)

    assert (
        not serializer.is_valid()
    ), f"Expected serializer to be invalid for a short or unexpected token: '{token_str}'"
    assert (
        "refresh" in serializer.errors
    ), "Expected error on 'refresh' field for malformed token."
