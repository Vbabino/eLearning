import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from hypothesis import given, settings, strategies as st
from accounts.models import CustomUser
from courses.models import Course
import uuid


@pytest.mark.django_db
@given(
    title=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
@settings(deadline=None)
def test_course_delete_view_positive(title):
    """
    Positive test: The teacher who created the course should be able to delete it.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    course = Course.objects.create(title=title, description="Test desc", teacher=teacher)
    url = reverse("course-delete", kwargs={"pk": course.id})

    response = client.delete(url)
    assert response.status_code == 204, f"Expected 204, got {response.status_code}"
    assert not Course.objects.filter(id=course.id).exists(), "Course should be deleted"

@pytest.mark.django_db
def test_course_delete_view_negative_not_owner():
    """
    Negative test: A different teacher or a non-teacher cannot delete a course they don't own.
    """
    client = APIClient()
    owner = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="ownerpass", user_type="teacher"
    )
    other_teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="otherpass", user_type="teacher"
    )
    course = Course.objects.create(title="Sample Course", description="Desc", teacher=owner)
    client.force_authenticate(user=other_teacher)

    url = reverse("course-delete", kwargs={"pk": course.id})
    response = client.delete(url)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    assert Course.objects.filter(id=course.id).exists(), "Course should not be deleted"

@pytest.mark.django_db
def test_course_delete_view_edge_case_nonexistent_course():
    """
    Edge case: Try to delete a course that does not exist, expecting a 404.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="teacherpass3",
        user_type="teacher",
    )
    client.force_authenticate(user=teacher)

    url = reverse("course-delete", kwargs={"pk": 99999})
    response = client.delete(url)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
