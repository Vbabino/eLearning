import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser

@pytest.mark.django_db
def test_request_password_reset_view_positive():
    """
    Positive test: An existing user with a valid email should receive a 200 response
    and a message indicating OTP was sent.
    """
    client = APIClient()
    url = reverse("request_password_reset")

    # Create user
    email = f"{uuid.uuid4()}@example.com"
    CustomUser.objects.create_user(
        email=email,
        password="somePassword123",
        user_type="student",
    )

    data = {"email": email}
    response = client.post(url, data=data, format="json")

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.json()}"
    )
    response_data = response.json()
    assert response_data.get("message") == "OTP sent to email.", "Expected OTP confirmation message."


@pytest.mark.django_db
def test_request_password_reset_view_negative_user_not_found():
    """
    Negative test: A request with a non-existent email should fail with 400 response.
    """
    client = APIClient()
    url = reverse("request_password_reset")

    non_existent_email = f"{uuid.uuid4()}@example.com"

    data = {"email": non_existent_email}
    response = client.post(url, data=data, format="json")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.json()}"
    )
    # Check error message
    assert "User with this email does not exist." in str(response.json()), (
        "Expected error message indicating user does not exist."
    )


@pytest.mark.django_db
def test_request_password_reset_view_edge_case_extremely_long_email():
    """
    Edge case: A request with an extremely long local part of the email
    may pass or fail based on DB/EmailField constraints. We test how the system handles it.
    """
    client = APIClient()
    url = reverse("request_password_reset")

    # Attempt an extremely long email local part
    long_local_part = "a" * 256
    long_email = f"{long_local_part}@example.com"

    user_created = False
    try:
        CustomUser.objects.create_user(
            email=long_email,
            password="somePassword456",
            user_type="teacher",
        )
        user_created = True
    except Exception:
        pass

    data = {"email": long_email}
    response = client.post(url, data=data, format="json")

    if user_created:
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}, Response: {response.json()}"
        )
        assert response.json().get("message") == "OTP sent to email.", (
            "Expected OTP confirmation message for an existing user."
        )
    else:
        assert response.status_code == 400, (
            f"Expected 400, got {response.status_code}, Response: {response.json()}"
        )
        assert "User with this email does not exist." in str(response.json()), (
            "Expected error message indicating user does not exist."
        )
