import uuid
import pytest
from hypothesis import given, strategies as st, settings
from accounts.models import CustomUser
from courses.models import Course
from feedback.serializers import FeedbackSerializer


@pytest.mark.django_db
@settings(deadline=None)
@given(
    comment_text=st.text(
        min_size=6,
        max_size=100,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )
)
def test_feedback_serializer_positive(comment_text):
    """
    Positive test: Valid FeedbackSerializer data should be valid and able to be saved.
    """
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        user_type="teacher",
    )

    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        user_type="student",
    )
    course = Course.objects.create(
        title="Test Course", description="Course Description", teacher=teacher
    )
    data = {
        "student": student.id,
        "course": course.id,
        "comment": comment_text,
    }
    serializer = FeedbackSerializer(data=data)
    assert (
        serializer.is_valid()
    ), f"Serializer should be valid. Errors: {serializer.errors}"
    feedback = serializer.save()
    assert feedback.comment == comment_text, "Feedback comment should match the input."


@pytest.mark.django_db
def test_feedback_serializer_negative_missing_comment():
    """
    Negative test: Missing the 'comment' field should make the serializer invalid.
    """
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        user_type="teacher",
    )

    student = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword456",
        user_type="teacher",
    )
    course = Course.objects.create(
        title="Sample Course", description="Course Desc", teacher=teacher
    )
    data = {
        "student": student.id,
        "course": course.id,
        # 'comment' is omitted
    }
    serializer = FeedbackSerializer(data=data)
    assert not serializer.is_valid(), "Serializer should be invalid without comment."
    assert (
        "comment" in serializer.errors
    ), "Expected an error for missing 'comment' field."


@pytest.mark.django_db
def test_feedback_serializer_edge_case_invalid_student():
    """
    Edge case: Providing an invalid student ID should make the serializer invalid.
    """
    teacher = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword123",
        user_type="teacher",
    )
    # Create a course
    course = Course.objects.create(
        title="Invalid Student Course", description="Course Desc", teacher=teacher
    )
    invalid_student_id = 99999
    data = {
        "student": invalid_student_id,
        "course": course.id,
        "comment": "This is a test comment.",
    }
    serializer = FeedbackSerializer(data=data)
    assert (
        not serializer.is_valid()
    ), "Serializer should be invalid with an invalid student ID."
    assert (
        "student" in serializer.errors
    ), "Expected an error for invalid 'student' field."
