import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser
from notifications.models import Notification

@pytest.mark.django_db
def test_notification_list_view_positive():
    """
    Positive test: An authenticated user should be able to retrieve their notifications.
    """
    client = APIClient()

    # Create a user and authenticate
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        user_type="student",
    )
    client.force_authenticate(user=user)

    # Create notifications for the user
    Notification.objects.create(user=user, content="New notification")
    Notification.objects.create(user=user, content="Another notification")

    url = reverse("notification-list")
    response = client.get(url)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.content}"
    )
    response_data = response.json()
    assert len(response_data) == 2, "Expected two notifications in the response."
    

@pytest.mark.django_db
def test_notification_list_view_negative_unauthenticated():
    """
    Negative test: An unauthenticated user should not be able to retrieve notifications.
    """
    client = APIClient()

    # Create a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword456",
        user_type="teacher",
    )

    # Create notifications for the user
    Notification.objects.create(user=user, content="Test notification")

    url = reverse("notification-list")
    response = client.get(url)

    assert response.status_code in [401, 403], (
        f"Expected 401 or 403, got {response.status_code}, Response: {response.content}"
    )


@pytest.mark.django_db
def test_notification_list_view_edge_case_no_notifications():
    """
    Edge case: An authenticated user with no notifications should receive an empty list.
    """
    client = APIClient()

    # Create a user and authenticate
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword789",
        user_type="student",
    )
    client.force_authenticate(user=user)

    url = reverse("notification-list")
    response = client.get(url)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.content}"
    )
    response_data = response.json()
    assert len(response_data) == 0, "Expected zero notifications in the response."
