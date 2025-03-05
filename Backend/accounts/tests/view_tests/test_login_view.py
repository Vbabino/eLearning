import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser

@pytest.mark.django_db
def test_login_view_positive():
    """
    Positive test: Valid credentials for an existing user should return tokens and user info.
    """
    client = APIClient()
    url = reverse("login")

    email = f"{uuid.uuid4()}@example.com"
    password = "someValidPass123"

    # Create user
    CustomUser.objects.create_user(
        email=email,
        password=password,
        first_name="Test",
        last_name="User",
        user_type="student"
    )

    data = {"email": email, "password": password}
    response = client.post(url, data=data, format="json")

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.json()}"
    )
    # Check tokens
    response_data = response.json()
    assert "access" in response_data, "Expected 'access' token in response."
    assert "refresh" in response_data, "Expected 'refresh' token in response."
    assert "user" in response_data, "Expected 'user' info in response."
    assert response_data["user"]["email"] == email, "Returned user email does not match."


@pytest.mark.django_db
def test_login_view_negative_wrong_credentials():
    """
    Negative test: Logging in with wrong credentials should fail.
    """
    client = APIClient()
    url = reverse("login")

    # Create a user
    email = f"{uuid.uuid4()}@example.com"
    correct_password = "correctPass"
    CustomUser.objects.create_user(
        email=email,
        password=correct_password,
        first_name="John",
        last_name="Doe",
        user_type="teacher"
    )

    # Provide wrong password
    data = {"email": email, "password": "wrongPass"}
    response = client.post(url, data=data, format="json")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.content}"
    )
    assert "Invalid credentials" in str(response.content), "Expected 'Invalid credentials' error."


@pytest.mark.django_db
def test_login_view_edge_case_no_email_provided():
    """
    Edge case: Attempt login with no email in the payload should fail validation.
    """
    client = APIClient()
    url = reverse("login")

    # Missing email field
    data = {"password": "testPass123"}
    response = client.post(url, data=data, format="json")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.content}"
    )
    message = response.json()
    assert "email" in message, "Expected an error about missing 'email' field."
