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
        max_size=20,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_user_search_view_positive(first_name):
    """
    Positive test: An authenticated user should be able to search for users
    using a filter (e.g., filtering by first_name). Expect HTTP 200 with matching results.
    """
    client = APIClient()

    # Create a user to authenticate
    auth_user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        first_name="Auth",
        last_name="User",
        user_type="teacher",
    )

    # Create a user to search for
    CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword456",
        first_name=first_name,
        last_name="Test",
        user_type="student",
    )

    # Authenticate
    client.force_authenticate(user=auth_user)

    url = reverse("user_search") + f"?first_name__icontains={first_name}"
    response = client.get(url)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.content}"
    )
    # Check search results
    results = response.json()
    # Expect the newly created user with that first_name to be in the results
    returned_first_names = [item["first_name"] for item in results]
    assert first_name in returned_first_names, (
        f"Expected user with first_name={first_name} in results."
    )


@pytest.mark.django_db
def test_user_search_view_negative_unauthenticated():
    """
    Negative test: An unauthenticated request should be disallowed (401 or 403).
    """
    client = APIClient()

    # Attempt a search without logging in
    url = reverse("user_search")
    response = client.get(url)

    assert response.status_code in [401, 403], (
        f"Expected 401 or 403, got {response.status_code}, Response: {response.content}"
    )


@pytest.mark.django_db
def test_user_search_view_edge_case_no_results():
    """
    Edge case: Searching with a filter that matches no users should yield an empty list.
    """
    client = APIClient()

    # Create a user to authenticate
    auth_user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        first_name="Authenticated",
        last_name="User",
        user_type="teacher",
    )
    client.force_authenticate(user=auth_user)

    # Perform a search with a keyword unlikely to match any user
    url = reverse("user_search") + "?first_name__icontains=NoSuchName"
    response = client.get(url)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.content}"
    )
    results = response.json()
    assert len(results) == 0, "Expected zero results for a non-matching filter."
