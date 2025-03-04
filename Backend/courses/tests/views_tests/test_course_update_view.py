import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from hypothesis import given, settings, strategies as st
from accounts.models import CustomUser
from courses.models import Course


@pytest.mark.django_db
@given(
    title=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
@settings(deadline=None)
def test_course_update_view_positive(title):
    """
    Positive test: The teacher who created the course should be able to update it.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    course = Course.objects.create(
        title="Old Title", description="Old Desc", teacher=teacher
    )
    url = reverse("course-update", kwargs={"pk": course.id})

    response = client.patch(url, {"title": title}, format="json")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    course.refresh_from_db()
    assert course.title == title


@pytest.mark.django_db
def test_course_update_view_negative_not_owner():
    """
    Negative test: A different teacher or a non-teacher cannot update this course.
    """
    client = APIClient()
    original_teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="origpass", user_type="teacher"
    )
    other_teacher = CustomUser.objects.create_user(
        email="other_teacher@example.com", password="otherpass", user_type="teacher"
    )
    client.force_authenticate(user=other_teacher)

    course = Course.objects.create(
        title="Some Title", description="Some Desc", teacher=original_teacher
    )
    url = reverse("course-update", kwargs={"pk": course.id})

    response = client.patch(url, {"title": "New Title"}, format="json")
    # Expect forbidden (403) because this teacher did not create the course
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


@pytest.mark.django_db
@given(
    long_title=st.text(
        min_size=102,
        max_size=120,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_course_update_view_edge_case_title_too_long(long_title):
    """
    Edge case: Attempt to update the course with a title exceeding the model's max_length (100).
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="teacherpass2",
        user_type="teacher",
    )
    client.force_authenticate(user=teacher)

    course = Course.objects.create(
        title="Valid Title", description="Valid Desc", teacher=teacher
    )
    url = reverse("course-update", kwargs={"pk": course.id})

    response = client.patch(url, {"title": long_title}, format="json")
    # If the title exceeds max_length=100, expect a 400 Bad Request or similar
    assert response.status_code in [
        400,
        413,
    ], f"Expected 400 or 413, got {response.status_code}"
