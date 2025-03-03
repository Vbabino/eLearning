import uuid
import pytest
from hypothesis import given, strategies as st
from accounts.models import CustomUser
from courses.models import Course, CourseMaterial
from courses.serializers import CourseMaterialSerializer


@pytest.mark.django_db
@given(
    file_name=st.text(min_size=5, max_size=50),
    description=st.text(min_size=5, max_size=100),
)
def test_course_material_serializer_positive(file_name, description):
    """Test CourseMaterialSerializer with valid data.

    This test ensures that the CourseMaterialSerializer correctly serializes
    the CourseMaterial instance with valid file_name and description.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testpass", user_type="teacher"
    )
    course = Course.objects.create(
        title="Test Course", description="A test course", teacher=user
    )
    course_material = CourseMaterial.objects.create(
        course=course, file_name=file_name, description=description
    )

    serializer = CourseMaterialSerializer(course_material)
    data = serializer.data

    assert data["file_name"] == file_name
    assert data["description"] == description
    assert data["course"] == course.pk


@pytest.mark.django_db
@given(
    file_name=st.text(min_size=1, max_size=4),  # Too short to be valid
    description=st.text(min_size=1, max_size=4),  # Too short to be valid
)
def test_course_material_serializer_negative_invalid_data(file_name, description):
    """
    Attempt to create a CourseMaterial with invalid data.
    The serializer should fail validation.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testpass", user_type="teacher"
    )
    course = Course.objects.create(
        title="Invalid Test Course", description="Test", teacher=user
    )

    data = {"course": course.pk, "file_name": file_name, "description": description}
    serializer = CourseMaterialSerializer(data=data)
    assert not serializer.is_valid()
    # We expect 'file_name' or 'description' to be flagged as invalid
    assert "file_name" in serializer.errors or "description" in serializer.errors


@pytest.mark.django_db
@given(
    file_name=st.text(min_size=50, max_size=50),  # Test boundary condition
    description=st.text(min_size=100, max_size=100),  # Another boundary condition
)
def test_course_material_serializer_edge_case_boundary_lengths(file_name, description):
    """
    An edge case test for CourseMaterialSerializer using hypothesis,
    testing maximum allowed boundary lengths for file_name and description.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testpass", user_type="teacher"
    )
    course = Course.objects.create(
        title="Boundary Test Course", description="Test", teacher=user
    )
    course_material = CourseMaterial.objects.create(
        course=course, file_name=file_name, description=description
    )

    serializer = CourseMaterialSerializer(course_material)
    data = serializer.data

    assert data["file_name"] == file_name
    assert data["description"] == description
    assert data["course"] == course.pk
