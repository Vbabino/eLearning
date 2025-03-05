import uuid
import pytest
from hypothesis import given, strategies as st, settings
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import CustomUser
from accounts.utils import generate_valid_image

@pytest.mark.django_db
@settings(deadline=None)
@given(
    first_name=st.text(
        min_size=5,
        max_size=20,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_get_profile_photo_view_positive(first_name):
    """
    Positive test: An authenticated user retrieves another user's profile photo (or their own).
    Expect HTTP 200.
    """
    client = APIClient()

    # Create a user to retrieve
    target_user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        first_name=first_name,
        last_name="PhotoUser",
        user_type="student",
    )
    # Assign a small valid photo
    target_user.photo.save(
        "test_image.png",
        generate_valid_image(), 
    )

    # Create and authenticate another user (could be the same user also)
    auth_user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="anotherPassword123",
        user_type="student",
    )
    client.force_authenticate(user=auth_user)

    url = reverse("user_photo", kwargs={"pk": target_user.id})
    response = client.get(url)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.content}"
    )
    # Check if the returned data includes the photo field
    response_data = response.json()
    assert "photo" in response_data, "Expected 'photo' field in the response data."


@pytest.mark.django_db
def test_get_profile_photo_view_negative_unauthenticated():
    """
    Negative test: An unauthenticated request should not be able to get a user's photo.
    Expect HTTP 401 or 403 response.
    """
    client = APIClient()

    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="somePassword456",
        user_type="teacher",
    )

    url = reverse("user_photo", kwargs={"pk": user.id})
    response = client.get(url)

    assert response.status_code in [401, 403], (
        f"Expected 401 or 403, got {response.status_code}, Response: {response.content}"
    )


@pytest.mark.django_db
def test_get_profile_photo_view_edge_case_nonexistent_user():
    """
    Edge case: Attempt to retrieve photo of a user that doesn't exist.
    Expect HTTP 404.
    """
    client = APIClient()

    # Create and authenticate a user
    auth_user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="edgeCasePass789",
        user_type="student",
    )
    client.force_authenticate(user=auth_user)

    # Use an ID that doesn't exist in the DB
    nonexistent_id = 99999
    url = reverse("user_photo", kwargs={"pk": nonexistent_id})
    response = client.get(url)

    assert response.status_code == 404, (
        f"Expected 404, got {response.status_code}, Response: {response.content}"
    )
