import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser

@pytest.mark.django_db
def test_logout_view_positive():
    """
    Positive test: Providing a valid refresh token for an authenticated user
    should result in a 205 status code and successful logout message.
    """
    # Create and authenticate a user
    client = APIClient()
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testpass123", user_type="student"
    )
    refresh = RefreshToken.for_user(user)

    # Log out using the valid refresh token
    url = reverse("logout")
    data = {"refresh": str(refresh)}
    response = client.post(url, data=data, format="json")

    # Expect 205 Reset Content
    assert response.status_code == 205, (
        f"Expected 205, got {response.status_code}, Response: {response.content}"
    )
    assert response.json().get("message") == "Logout successful", "Expected success message."


@pytest.mark.django_db
def test_logout_view_negative_invalid_token():
    """
    Negative test: Providing an invalid or malformed refresh token should fail validation.
    """
    client = APIClient()
    url = reverse("logout")

    # This token does not conform to a valid format / is not from an actual user
    data = {"refresh": "invalid.token.string"}
    response = client.post(url, data=data, format="json")

    # Expect 400 (Bad Request) due to serializer error
    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.content}"
    )
    # Check error message
    assert "Invalid or expired refresh token." in str(response.content), (
        "Expected an invalid or expired token error."
    )


@pytest.mark.django_db
def test_logout_view_edge_case_empty_token():
    """
    Edge case: Providing an empty refresh token should also fail validation.
    """
    client = APIClient()
    url = reverse("logout")

    data = {"refresh": ""}
    response = client.post(url, data=data, format="json")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.content}"
    )
    # Check for the same or similar error message
    assert "This field may not be blank." in str(
        response.content
    ), "Expected an invalid or expired token error."
