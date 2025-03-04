import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser
from courses.models import Course, CourseMaterial

@pytest.mark.django_db
@settings(deadline=None)
@given(
    file_name=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    ),
    description=st.text(
        min_size=6,
        max_size=100,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    ),
)
def test_course_material_list_view_positive(file_name, description):
    """
    Positive test: A teacher can view the materials of a course they own.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    # Create a course and associated materials
    course = Course.objects.create(title="Test Course", description="Test Desc", teacher=teacher)
    CourseMaterial.objects.create(course=course, file_name=file_name, description=description)

    # Hit the list endpoint
    url = reverse("course-material-list", kwargs={"pk": course.id})
    response = client.get(url)
    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.json()}"
    )
    # Check that the material appears in the response
    materials = response.json()
    assert len(materials) == 1, "Expected 1 course material in the list"
    assert materials[0]["file_name"] == file_name


@pytest.mark.django_db
def test_course_material_list_view_negative_unauthenticated():
    """
    Negative test: An unauthenticated user should not be able to view course materials.
    """
    client = APIClient()  # Not authenticated

    # Create a teacher and course
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    course = Course.objects.create(title="Private Course", description="No Access", teacher=teacher)

    url = reverse("course-material-list", kwargs={"pk": course.id})
    response = client.get(url)

    # Expect 401 (unauthorized) or 403 (forbidden)
    assert response.status_code in [401, 403], (
        f"Expected 401 or 403, got {response.status_code}, Response: {response.content}"
    )


@pytest.mark.django_db
def test_course_material_list_view_edge_case_no_materials():
    """
    Edge case: When a teacher has a course with no materials, the list should be empty.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass2", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    # Create a course but do not add any materials
    course = Course.objects.create(title="Empty Materials", description="No files", teacher=teacher)

    url = reverse("course-material-list", kwargs={"pk": course.id})
    response = client.get(url)
    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.json()}"
    )
    materials = response.json()
    assert len(materials) == 0, "Expected 0 course materials in the list"