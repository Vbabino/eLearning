import uuid
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from hypothesis import given, strategies as st, settings
from accounts.models import CustomUser
from courses.models import Course

@pytest.mark.django_db
@settings(deadline=None)
@given(
    course_title=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_search_course_view_positive(course_title):
    """
    Positive test: An authenticated user should be able to search for an existing course by title.
    """
    client = APIClient()

    # Create and authenticate a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="pass123", user_type="teacher"
    )
    client.force_authenticate(user=user)

    # Create a course with the given title
    Course.objects.create(title=course_title, description="Test course", teacher=user)

    url = reverse("course-search") + f"?title__iexact={course_title}"
    response = client.get(url)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.json()}"
    )
    results = response.json()
    assert len(results) == 1, "Expected exactly one course in the search results."
    assert results[0]["title"] == course_title, "Returned course title does not match."


@pytest.mark.django_db
def test_search_course_view_negative_unauthenticated():
    """
    Negative test: An unauthenticated user should not be able to search for courses.
    """
    client = APIClient()  # Not authenticated

    url = reverse("course-search") + "?title__iexact=Something"
    response = client.get(url)

    # Expect 401 or 403 depending on your authentication settings
    assert response.status_code in [401, 403], (
        f"Expected 401 or 403, got {response.status_code}, Response: {response.content}"
    )


@pytest.mark.django_db
def test_search_course_view_edge_case_no_results():
    """
    Edge case: Searching for a string that doesn't match any course titles should return an empty list.
    """
    client = APIClient()

    # Create and authenticate a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="pass1234", user_type="teacher"
    )
    client.force_authenticate(user=user)

    # Create a course with a specific title
    Course.objects.create(title="KnownTitle", description="Test course", teacher=user)

    # Search for something that won't match
    url = reverse("course-search") + "?title__icontains=NoMatchString"
    response = client.get(url)
    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.content}"
    )
    results = response.json()
    assert len(results) == 0, "Expected zero courses in the search results."
