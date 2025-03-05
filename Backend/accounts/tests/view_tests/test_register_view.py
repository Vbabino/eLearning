import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser


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
def test_register_view_positive(first_name, last_name):
    """
    Positive test: Valid registration with all required fields.
    """
    client = APIClient()
    url = reverse("register")

    data = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "testpass123",
        "first_name": first_name,
        "last_name": last_name,
        "user_type": "student",
    }

    response = client.post(url, data=data, format="json")
    # 201 = created
    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}, Response: {response.json()}"
    # Check user creation
    created_email = response.json().get("email")
    assert CustomUser.objects.filter(
        email=created_email
    ).exists(), "User should exist in DB."


@pytest.mark.django_db
def test_register_view_negative_missing_password():
    """
    Negative test: Missing password should fail registration.
    """
    client = APIClient()
    url = reverse("register")

    data = {
        "email": f"{uuid.uuid4()}@example.com",
        "first_name": "Missing",
        "last_name": "Password",
        "user_type": "student",
    }

    response = client.post(url, data=data, format="json")
    # 400 = bad request due to serializer validation failure
    assert (
        response.status_code == 400
    ), f"Expected 400, got {response.status_code}, Response: {response.content}"
    assert "password" in response.json(), "Expected an error about missing password."


@pytest.mark.django_db
@settings(deadline=None)
@given(
    long_name=st.text(
        min_size=256,
        max_size=256,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_register_view_edge_case_long_first_name(long_name):
    """
    Edge case test: A very long first_name (exceeding 255 chars) should fail validation.
    """
    client = APIClient()
    url = reverse("register")

    data = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "testpass123",
        "first_name": long_name,
        "last_name": "NormalLast",
        "user_type": "teacher",
    }

    response = client.post(url, data=data, format="json")
    assert (
        response.status_code == 400
    ), f"Expected 400, got {response.status_code}, Response: {response.content}"
    errors = response.json()
    assert "first_name" in errors, "Expected an error for 'first_name' due to length."
