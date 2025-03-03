import uuid
import pytest
import string
from hypothesis import given, example
import hypothesis.strategies as st
from courses.models import Course
from accounts.models import CustomUser
from courses.serializers import CourseSerializer


@pytest.mark.django_db
@given(
    title=st.text(min_size=1, max_size=100),
    description=st.text(),
    teacher_email=st.emails(),
)
@example(
    title="Example Course",
    description="Example Description",
    teacher_email="teacher@example.com",
)
def test_course_serializer(title, description, teacher_email):
    """
    Positive case: Test the CourseSerializer with valid data.
    """
    CustomUser.objects.all().delete()
    Course.objects.all().delete()

    teacher = CustomUser.objects.create(
        email=f"{uuid.uuid4()}@example.com", user_type="teacher"
    )
    course = Course.objects.create(
        title=title, description=description, teacher=teacher
    )

    serializer = CourseSerializer(instance=course)

    assert serializer.data["title"] == title
    assert serializer.data["description"] == description


@pytest.mark.django_db
@given(
    title=st.just(""),
    description=st.text(min_size=500, max_size=1000),
    teacher_email=st.just("invalid-email"),
)
def test_course_serializer_invalid_data(title, description, teacher_email):
    """
    Test that the CourseSerializer rejects invalid data.
    """
    teacher = CustomUser.objects.create(
        email=f"{uuid.uuid4()}@example.com", user_type="teacher"
    )

    data = {
        "title": title,
        "description": description,
        "teacher": teacher.id,
    }

    serializer = CourseSerializer(data=data)

    assert not serializer.is_valid()
    assert "title" in serializer.errors or "description" in serializer.errors


@pytest.mark.django_db
@given(
    title=st.text(min_size=1, max_size=100, alphabet=string.printable),
    description=st.text(min_size=1, max_size=10000, alphabet=string.printable),
)
def test_course_serializer_edge_cases(title, description):
    """
    Test edge cases for the CourseSerializer using hypothesis.
    Uses string.printable alphabet to include special characters.
    """
    CustomUser.objects.all().delete()
    Course.objects.all().delete()

    teacher = CustomUser.objects.create(
        email=f"{uuid.uuid4()}@example.com", user_type="teacher"
    )

    course = Course.objects.create(
        title=title, description=description, teacher=teacher
    )

    serializer = CourseSerializer(instance=course)
    assert serializer.data["title"] == title
    assert serializer.data["description"] == description
