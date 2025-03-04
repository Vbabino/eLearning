import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from hypothesis import given, settings, strategies as st
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
@settings(deadline=None)
def test_course_enroll_view_positive(course_title):
    """
    Positive test: A student can enroll in a valid course they are not already enrolled in.
    """
    client = APIClient()

    # Create a teacher and a course
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    course = Course.objects.create(title=course_title, description="Test desc", teacher=teacher)

    # Create a student and authenticate
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )
    client.force_authenticate(user=student)

    url = reverse("course-enroll", kwargs={"pk": course.id})
    response = client.post(url, {"student": student.id, "course": course.id}, format="json")
    assert response.status_code == 201, f"Expected 201, got {response.status_code}, Response: {response.json()}"
    assert Enrollment.objects.filter(student=student, course=course, is_active=True).exists()


@pytest.mark.django_db
def test_course_enroll_view_negative_non_student():
    """
    Negative test: A non-student (e.g., teacher) should not be able to enroll in a course.
    """
    client = APIClient()

    # Create a teacher and a course
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="teacherpass2",
        user_type="teacher",
    )
    course = Course.objects.create(title="Sample Course", description="Desc", teacher=teacher)

    # Another teacher tries to enroll
    other_teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="teacherpass3",
        user_type="teacher",
    )
    client.force_authenticate(user=other_teacher)

    url = reverse("course-enroll", kwargs={"pk": course.id})
    response = client.post(url, {}, format="json")
    # Should be forbidden (403) due to IsStudent permission
    assert response.status_code == 403, f"Expected 403, got {response.status_code}, Response: {response.json()}"


@pytest.mark.django_db
def test_course_enroll_view_edge_case_non_existent_course():
    """
    Edge case: Attempting to enroll in a course that doesn't exist should return 404.
    """
    client = APIClient()

    # Create a student and authenticate
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="studentpass4",
        user_type="student",
    )
    client.force_authenticate(user=student)

    non_existent_course_id = 99999
    url = reverse("course-enroll", kwargs={"pk": non_existent_course_id})
    response = client.post(url, {"student": student.id, "course": non_existent_course_id}, format="json")

    # Using .get() on a nonexistent course triggers a 404
    assert response.status_code == 404, f"Expected 404, got {response.status_code}, Response: {response.json()}"
