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
def test_course_list_view_for_students_positive(course_title):
    """
    Positive test: a student enrolled in a course should see it in the list.
    """
    client = APIClient()
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )
    client.force_authenticate(user=student)

    # Create a course and enroll the student
    course = Course.objects.create(
        title=course_title, description="Test Description", teacher=student
    )
    Enrollment.objects.create(student=student, course=course, is_active=True)

    url = reverse("course-list-students")
    response = client.get(url)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert len(response.data) == 1, "Expected one course in the response"
    assert response.data[0]["title"] == course_title


@pytest.mark.django_db
def test_course_list_view_for_students_negative_non_student():
    """
    Negative test: a non-student (teacher) should be forbidden (403).
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    url = reverse("course-list-students")
    response = client.get(url)

    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


@pytest.mark.django_db
def test_course_list_view_for_students_edge_case_no_enrollments():
    """
    Edge case: a student with no enrollments should see a custom message.
    """
    client = APIClient()
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="studentpass2",
        user_type="student",
    )
    client.force_authenticate(user=student)

    url = reverse("course-list-students")
    response = client.get(url)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "message" in response.data, "Expected a custom message in the response"
    assert response.data["message"] == "You are not enrolled in any courses."
