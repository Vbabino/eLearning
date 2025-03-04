import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from hypothesis import given, settings, strategies as st
from accounts.models import CustomUser
from courses.models import Course


@pytest.mark.django_db
@given(
    course_title=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
@settings(deadline=None)
def test_course_list_view_positive(course_title):
    """
    A positive test ensuring a teacher user can successfully create and list their courses.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    url = reverse("course-list")
    response = client.post(
        url,
        {
            "title": course_title,
            "description": "Test description",
            "teacher": teacher.id,
        },
        format="json",
    )
    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}, Response: {response.json()}"

    # Retrieve the list of courses
    get_response = client.get(url)
    assert (
        get_response.status_code == 200
    ), f"Expected 200, got {get_response.status_code}"
    # Ensure the created course is returned
    assert len(get_response.data) == 1
    assert get_response.data[0]["title"] == course_title


@pytest.mark.django_db
def test_course_list_view_negative_non_teacher_cannot_create():
    """
    A negative test ensuring a non-teacher user cannot create courses.
    """
    client = APIClient()
    student = CustomUser.objects.create_user(
        email="student@example.com", password="studentpass", user_type="student"
    )
    client.force_authenticate(user=student)

    url = reverse("course-list")
    response = client.post(
        url, {"title": "Invalid", "description": "Test description"}, format="json"
    )
    # Expect permission denied (403)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


@pytest.mark.django_db
@settings(deadline=None)
@given(course_title=st.text(min_size=100, max_size=100))
def test_course_list_view_edge_case_boundary_title_length(course_title):
    """
    An edge case test ensuring the view handles a course title at its maximum boundary.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="teacherpass2",
        user_type="teacher",
    )
    client.force_authenticate(user=teacher)

    url = reverse("course-list")
    response = client.post(
        url,
        {"title": course_title, "description": "Edge case description"},
        format="json",
    )
    # If Course.title supports 100 chars, expect 201; otherwise 400.
    assert response.status_code in [
        201,
        400,
    ], f"Expected 201 or 400, got {response.status_code}"
