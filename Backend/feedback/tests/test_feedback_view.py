import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser
from courses.models import Course
from feedback.models import Feedback

@pytest.mark.django_db
@settings(deadline=None)
@given(
    comment_text=st.text(
        min_size=6,
        max_size=100,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
    )
)
def test_feedback_view_positive(comment_text):
    """
    Positive test: A student can submit valid feedback for a course.
    """
    client = APIClient()

    # Create a student and authenticate
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        user_type="student",
    )
    client.force_authenticate(user=student)

    # Create a course
    course = Course.objects.create(
        title="Test Course",
        description="Course Description",
        teacher=student,
    )

    url = reverse("feedback")
    data = {
        "student": student.id,
        "course": course.id,
        "comment": comment_text,
    }
    response = client.post(url, data=data, format="json")

    assert response.status_code == 201, (
        f"Expected 201, got {response.status_code}, Response: {response.json()}"
    )
    feedback = Feedback.objects.get(course=course, student=student)
    assert feedback.comment == comment_text, "Feedback comment should match the input."


@pytest.mark.django_db
def test_feedback_view_negative_unauthenticated():
    """
    Negative test: An unauthenticated user should not be able to submit feedback.
    """
    client = APIClient()

    # Create a student
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword456",
        user_type="student",
    )

    # Create a course
    course = Course.objects.create(
        title="Sample Course",
        description="Course Description",
        teacher=student,
    )

    url = reverse("feedback")
    data = {
        "course": course.id,
        "comment": "This is a test comment.",
    }
    response = client.post(url, data=data, format="json")

    assert response.status_code in [401, 403], (
        f"Expected 401 or 403, got {response.status_code}, Response: {response.content}"
    )


@pytest.mark.django_db
def test_feedback_view_edge_case_empty_comment():
    """
    Edge case: Submitting feedback with an empty comment should fail validation.
    """
    client = APIClient()

    # Create a student and authenticate
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword789",
        user_type="student",
    )
    client.force_authenticate(user=student)

    # Create a course
    course = Course.objects.create(
        title="Edge Case Course",
        description="Course Description",
        teacher=student,
    )

    url = reverse("feedback")
    data = {
        "course": course.id,
        "comment": "",  # Empty comment
    }
    response = client.post(url, data=data, format="json")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.content}"
    )
    assert "comment" in response.json(), "Expected validation error for 'comment' field."