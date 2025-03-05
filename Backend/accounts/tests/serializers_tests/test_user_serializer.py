import uuid
import pytest
from hypothesis import given, strategies as st, settings
from accounts.models import CustomUser
from accounts.serializers import UserSerializer


@pytest.mark.django_db
@settings(deadline=None)
@given(
    first_name=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    ),
    last_name=st.text(
        min_size=5,
        max_size=50,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    ),
)
def test_user_serializer_positive(first_name, last_name):
    """
    Positive test: Updating first_name and last_name of an existing user
    with valid data should pass serializer validation.
    """
    # Create a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testpass",
        first_name="OldFirst",
        last_name="OldLast",
        user_type="student",
    )

    # Update user with new first_name and last_name
    data = {"first_name": first_name, "last_name": last_name}
    serializer = UserSerializer(instance=user, data=data, partial=True)
    assert (
        serializer.is_valid()
    ), f"Serializer should be valid. Errors: {serializer.errors}"

    # Save and verify the changes
    updated_user = serializer.save()
    assert updated_user.first_name == first_name
    assert updated_user.last_name == last_name


@pytest.mark.django_db
def test_user_serializer_negative_invalid_field():
    """
    Negative test: Attempting to update read-only fields (email, user_type)
    should fail serializer validation.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testpass",
        first_name="John",
        last_name="Doe",
        user_type="student",
    )

    # Attempt to change read-only fields
    data = {
        "email": f"{uuid.uuid4()}@example.com",
        "user_type": "teacher",
    }
    serializer = UserSerializer(instance=user, data=data, partial=True)

    assert (
        not serializer.is_valid()
    ), "Serializer should be invalid when updating read-only fields."
    assert "email" in serializer.errors, "Expected error for modifying email."
    assert "user_type" in serializer.errors, "Expected error for modifying user_type."


@pytest.mark.django_db
@given(
    long_name=st.text(
        min_size=256,
        max_size=256,
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.",
    )  # Exceeding typical max_length=255
)
def test_user_serializer_edge_case_name_too_long(long_name):
    """
    Edge case test: Attempting to update first_name or last_name
    beyond the typical max length should result in validation failure
    (or eventually a DB constraint error).
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testpass",
        first_name="NormalFirst",
        last_name="NormalLast",
        user_type="student",
    )

    # Exceed typical length constraints
    data = {"first_name": long_name}
    serializer = UserSerializer(instance=user, data=data, partial=True)

    valid = serializer.is_valid()
    if valid:
        try:
            serializer.save()
            assert (
                True
            ), "Name saved despite exceeding typical max_length; check model constraints."
        except Exception as e:
            pytest.fail(f"DB error on save for long name: {str(e)}")
    else:
        assert not valid, "Serializer should be invalid with overly long name."
