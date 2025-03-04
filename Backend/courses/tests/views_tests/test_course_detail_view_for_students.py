import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from hypothesis import given, strategies as st
from accounts.models import CustomUser
from courses.models import Course, Enrollment


@pytest.mark.django_db
@given(
    course_title=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_course_detail_view_for_students_positive(course_title):
    """
    Positive test: a student can view details of an existing course they enroll in.
    """
    client = APIClient()
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )
    client.force_authenticate(user=student)

    course = Course.objects.create(
        title=course_title, description="A test course", teacher=student
    )
    Enrollment.objects.create(student=student, course=course, is_active=True)

    url = reverse("course-detail", kwargs={"pk": course.id})
    response = client.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.data["title"] == course_title


@pytest.mark.django_db
def test_course_detail_view_for_students_negative_unauthenticated():
    """
    Negative test: an unauthenticated user should not be able to access the course detail view.
    """
    client = APIClient()
    # No authentication
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    course = Course.objects.create(
        title="Test Course", description="A test course", teacher=teacher
    )

    url = reverse("course-detail", kwargs={"pk": course.id})
    response = client.get(url)
    # Expect 403 (forbidden) or 401 (unauthorized)
    assert response.status_code in [
        401,
        403,
    ], f"Expected 401 or 403, got {response.status_code}"


@pytest.mark.django_db
def test_course_detail_view_for_students_edge_case_course_not_found():
    """
    Edge case: a student attempts to view details of a non-existent course, expecting a 404.
    """
    client = APIClient()
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="studentpass2",
        user_type="student",
    )
    client.force_authenticate(user=student)

    non_existent_course_id = 9999
    url = reverse("course-detail", kwargs={"pk": non_existent_course_id})
    response = client.get(url)

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
