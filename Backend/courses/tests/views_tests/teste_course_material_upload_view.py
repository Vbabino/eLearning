import uuid
import pytest
from hypothesis import given, strategies as st, settings
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser
from courses.models import Course, CourseMaterial
import io
from django.core.files.uploadedfile import SimpleUploadedFile


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
def test_course_material_upload_view_positive(file_name, description):
    """
    Positive test: A teacher can upload valid course material.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    course = Course.objects.create(
        title="Test Course", description="Test Description", teacher=teacher
    )

    url = reverse("course-material-upload", kwargs={"pk": course.id})

    # Simulate a file upload
    file_content = io.BytesIO(b"dummy data")
    file = SimpleUploadedFile(
        "test_file.pdf", file_content.read(), content_type="application/pdf"
    )

    data = {
        "course": course.id,
        "file_name": file_name,
        "description": description,
        "file": file,
    }

    response = client.post(url, data, format="multipart")
    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}, Response: {response.json()}"
    assert CourseMaterial.objects.filter(
        course=course, file_name=file_name
    ).exists(), "The uploaded course material should exist in the database."


@pytest.mark.django_db
def test_course_material_upload_view_negative_no_permission():
    """
    Negative test: A non-teacher (student) should not be able to upload course material.
    """
    client = APIClient()
    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="studentpass", user_type="student"
    )
    client.force_authenticate(user=student)

    course = Course.objects.create(
        title="Forbidden Course", description="No Access", teacher=student
    )

    url = reverse("course-material-upload", kwargs={"pk": course.id})
    # Simulate a file upload
    file_content = io.BytesIO(b"dummy data")
    file = SimpleUploadedFile(
        "test_file.pdf", file_content.read(), content_type="application/pdf"
    )

    data = {
        "course": course.id,
        "file_name": "Test File",
        "description": "Test description",
        "file": file,
    }

    response = client.post(url, data, format="multipart")
    assert (
        response.status_code == 403
    ), f"Expected 403, got {response.status_code}, Response: {response.content}"


@pytest.mark.django_db
@settings(deadline=None)
@given(
    # Generate a file_name that exceeds the max_length=255 limit
    file_name=st.text(min_size=256, max_size=256),
    description=st.text(min_size=6, max_size=20),
)
def test_course_material_upload_view_edge_case_file_name_too_long(
    file_name, description
):
    """
    Edge case test: Attempting to upload material with file_name longer than 255 chars.
    """
    client = APIClient()
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="teacherpass", user_type="teacher"
    )
    client.force_authenticate(user=teacher)

    course = Course.objects.create(
        title="Edge Course", description="Edge Description", teacher=teacher
    )

    url = reverse("course-material-upload", kwargs={"pk": course.id})
    # Simulate a file upload
    file_content = io.BytesIO(b"dummy data")
    file = SimpleUploadedFile(
        "test_file.pdf", file_content.read(), content_type="application/pdf"
    )

    data = {
        "course": course.id,
        "file_name": file_name,
        "description": description,
        "file": file,
    }

    response = client.post(url, data, format="multipart")
    assert (
        response.status_code == 400
    ), f"Expected 400, got {response.status_code}, Response: {response.content}"
