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
def test_unblock_student_view_positive(course_title):
    """
    Positive test: The teacher who owns the course can unblock an enrolled student.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )
    client.force_authenticate(user=teacher)

    # Create a course and enroll the student
    course = Course.objects.create(
        title=course_title, description="Test Desc", teacher=teacher
    )
    enrollment = Enrollment.objects.create(
        student=student, course=course, is_active=True
    )

    # unblock the student
    url = reverse(
        "unblock-student",
        kwargs={"course_id": course.id, "pk": enrollment.id},
    )
    data = {"is_active": True, "student": student.id, "course": course.id}
    response = client.put(url, data, format="json")
    assert (
        response.status_code == 200
    ), f"Expected 200, got {response.status_code}, Response: {response.json()}"
    enrollment.refresh_from_db()
    assert enrollment.is_active, "Enrollment should be active after unblocking."


@pytest.mark.django_db
def test_unblock_student_view_negative_not_owner():
    """
    Negative test: Another teacher (not the course owner) tries to unblock a student.
    """
    client = APIClient()
    owner_teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="ownerpass", user_type="teacher"
    )
    other_teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="otherpass", user_type="teacher"
    )
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )

    course = Course.objects.create(
        title="OwnerCourse", description="Owner Desc", teacher=owner_teacher
    )
    enrollment = Enrollment.objects.create(
        student=student, course=course, is_active=True
    )

    client.force_authenticate(user=other_teacher)
    url = reverse(
        "unblock-student",
        kwargs={"course_id": course.id, "pk": enrollment.id},
    )

    data = {"is_active": True, "student": student.id, "course": course.id}

    response = client.put(
        url,
        data,
        format="json",
    )
    assert (
        response.status_code == 403
    ), f"Expected 403, got {response.status_code}, Response: {response.content}"
    enrollment.refresh_from_db()
    assert enrollment.is_active, "Enrollment should remain active."


@pytest.mark.django_db
def test_unblock_student_view_edge_case_non_existent_enrollment():
    """
    Edge case: Attempt to unblock a student from a non-existent enrollment should return 404.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="teacherpass2",
        user_type="teacher",
    )
    client.force_authenticate(user=teacher)

    # Create a course without any enrollment
    course = Course.objects.create(
        title="No Student", description="No Enrollments", teacher=teacher
    )

    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )

    # Try removing enrollment with a non-existent pk=9999
    url = reverse(
        "unblock-student",
        kwargs={"course_id": course.id, "pk": 9999},
    )
    data = {"is_active": True, "student": student.id, "course": course.id}
    response = client.put(url, data, format="json")
    assert (
        response.status_code == 404
    ), f"Expected 404, got {response.status_code}, Response: {response.content}"
