import uuid
import pytest
from hypothesis import given, strategies as st, settings
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import CustomUser

@pytest.mark.django_db
@settings(deadline=None)
@given(
    first_name=st.text(
        min_size=5,
        max_size=20,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    ),
    last_name=st.text(
        min_size=5,
        max_size=20,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    ),
)
def test_user_detail_view_positive(first_name, last_name):
    """
    Positive test: An authenticated user should be able to retrieve and update their own profile.
    """
    # Create and authenticate user
    client = APIClient()
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testpass123",
        first_name="InitialFirst",
        last_name="InitialLast",
        user_type="student",
    )
    client.force_authenticate(user=user)

    # Retrieve user detail
    url = reverse("user_detail", kwargs={"pk": user.id})
    get_response = client.get(url)
    assert get_response.status_code == 200, (
        f"Expected 200, got {get_response.status_code}, Response: {get_response.content}"
    )

    # Update user detail
    data_to_update = {"first_name": first_name, "last_name": last_name}
    put_response = client.put(url, data=data_to_update, format="json")
    assert put_response.status_code == 200, (
        f"Expected 200, got {put_response.status_code}, Response: {put_response.content}"
    )
    updated_user = CustomUser.objects.get(id=user.id)
    assert updated_user.first_name == first_name, "First name should be updated."
    assert updated_user.last_name == last_name, "Last name should be updated."


@pytest.mark.django_db
def test_user_detail_view_negative_unauthenticated():
    """
    Negative test: An unauthenticated user should not access user detail.
    """
    client = APIClient()

    # Create a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testpass456",
        first_name="UnauthTest",
        last_name="User",
        user_type="teacher",
    )

    url = reverse("user_detail", kwargs={"pk": user.id})
    response = client.get(url)
    assert response.status_code in [401, 403], (
        f"Expected 401 or 403, got {response.status_code}, Response: {response.content}"
    )


@pytest.mark.django_db
def test_user_detail_view_edge_case_read_only_fields():
    """
    Edge case: Attempting to update read-only fields (email, user_type) should fail serializer validation.
    """
    client = APIClient()
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testpass789",
        first_name="ReadOnlyCase",
        last_name="Edge",
        user_type="student",
    )
    client.force_authenticate(user=user)

    url = reverse("user_detail", kwargs={"pk": user.id})
    data_to_update = {
        "email": f"{uuid.uuid4()}@example.com",  # read-only
        "user_type": "teacher",  # read-only
        "first_name": "NewFirst",
        "last_name": "NewLast",
    }
    response = client.put(url, data=data_to_update, format="json")
    # Expect a 400 due to serializer read-only field validation
    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.content}"
    )

    response_data = response.json()
    # Verify that serializer complains about read-only fields
    assert "email" in response_data or "user_type" in response_data, (
        "Expected serializer error for read-only fields."
    )