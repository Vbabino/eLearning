import uuid
import pytest
from hypothesis import given, strategies as st
from rest_framework.test import APIRequestFactory
from accounts.models import CustomUser
from courses.models import Course, Enrollment
from courses.serializers import EnrollmentSerializer

@pytest.mark.django_db
@given(st.text(min_size=1, max_size=50))
def test_enrollment_serializer_positive(course_title):
    """
    Test the EnrollmentSerializer for positive cases.

    This test ensures that the EnrollmentSerializer correctly serializes the enrollment data
    for a given course and user.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="pass123"
    )
    course = Course.objects.create(title=course_title, description="Test", teacher=user)
    enrollment = Enrollment.objects.create(student=user, course=course, is_active=True)

    request = APIRequestFactory().get("/")
    request.user = user
    serializer = EnrollmentSerializer(enrollment, context={"request": request})
    data = serializer.data

    assert data["course_title"] == course_title
    assert data["student_details"]["email"] == user.email
    assert data["is_enrolled"] is True


@pytest.mark.django_db
def test_enrollment_serializer_negative_invalid_data():
    """
    Attempt to create an Enrollment with missing required fields.
    The serializer should fail validation.
    """
    data = {
        "student": None,
        "course": None,
        "is_active": True
    }
    serializer = EnrollmentSerializer(data=data)
    assert not serializer.is_valid()
    assert "student" in serializer.errors
    assert "course" in serializer.errors

@pytest.mark.django_db
def test_enrollment_serializer_edge_case_inactive_enrollment():
    """
    Ensure serializer handles an Enrollment correctly when is_active is False.
    """
    user = CustomUser.objects.create_user(email="edge@example.com", password="pass123")
    course = Course.objects.create(title="Edge Case Course", description="Test", teacher=user)
    enrollment = Enrollment.objects.create(student=user, course=course, is_active=False)

    request = APIRequestFactory().get("/")
    request.user = user
    serializer = EnrollmentSerializer(enrollment, context={"request": request})
    data = serializer.data

    assert data["is_enrolled"] is False


@pytest.mark.django_db
@given(st.text(min_size=50, max_size=50))
def test_enrollment_serializer_edge_case_boundary_title_length(course_title):
    """
    An edge case test for EnrollmentSerializer using hypothesis, testing
    a course title at its maximum allowed boundary (50 chars).
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="pass123"
    )
    course = Course.objects.create(title=course_title, description="Test", teacher=user)
    enrollment = Enrollment.objects.create(student=user, course=course, is_active=True)

    request = APIRequestFactory().get("/")
    request.user = user
    serializer = EnrollmentSerializer(enrollment, context={"request": request})
    data = serializer.data

    assert data["course_title"] == course_title
    assert data["student_details"]["email"] == user.email
    assert data["is_enrolled"] is True