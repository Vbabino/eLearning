import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser
from courses.models import Course, Enrollment

@pytest.mark.django_db
@settings(deadline=None)
@given(
    course_title=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_teacher_enrolled_students_view_positive(course_title):
    """
    Positive test: A teacher can view the students enrolled in their course.
    """
    client = APIClient()

    # Create a teacher and authenticate
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    # Create a student
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )

    # Create a course for the teacher and enroll the student
    course = Course.objects.create(title=course_title, description="Test Desc", teacher=teacher)
    Enrollment.objects.create(student=student, course=course, is_active=True)

    url = reverse("teacher-students")
    response = client.get(url)

    assert (
        response.status_code == 200
    ), f"Expected 200, got {response.status_code}, Response: {response.content}"
    enrolled_list = response.json()
    assert len(enrolled_list) == 1, "There should be exactly one enrolled student"
    assert enrolled_list[0]["student_details"]["email"] == student.email


@pytest.mark.django_db
def test_teacher_enrolled_students_view_negative_non_teacher():
    """
    Negative test: A non-teacher (e.g. a student) should not be able to view enrolled students.
    """
    client = APIClient()

    # Create a student (non-teacher) and authenticate
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )
    client.force_authenticate(user=student)

    url = reverse("teacher-students")
    response = client.get(url)

    # Expected 403 due to IsTeacher permission
    assert (
        response.status_code == 403
    ), f"Expected 403, got {response.status_code}, Response: {response.content}"


@pytest.mark.django_db
def test_teacher_enrolled_students_view_edge_case_no_enrollments():
    """
    Edge case: A teacher with no enrollments should receive an empty list.
    """
    client = APIClient()

    # Create a teacher with no enrollments
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    url = reverse("teacher-students")
    response = client.get(url)

    assert (
        response.status_code == 200
    ), f"Expected 200, got {response.status_code}, Response: {response.content}"
    enrolled_list = response.json()
    assert len(enrolled_list) == 0, "Expected no enrollments in the response"