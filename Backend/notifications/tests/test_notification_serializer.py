import uuid
import pytest
from hypothesis import given, strategies as st, settings
from accounts.models import CustomUser
from notifications.serializers import NotificationSerializer

@pytest.mark.django_db
def test_notification_serializer_positive():
    """
    Positive test: Valid NotificationSerializer data should be valid and able to be saved.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testPassword123", user_type="student"
    )
    content_text = "This is a test notification."
    
    data = {
        "user": user.id,
        "content": content_text,
    }
    serializer = NotificationSerializer(data=data)
    assert serializer.is_valid(), f"Serializer should be valid. Errors: {serializer.errors}"
    notification = serializer.save()
    assert notification.content == content_text, "Notification content should match the input."


@pytest.mark.django_db
def test_notification_serializer_negative_missing_content():
    """
    Negative test: Missing the 'content' field should make the serializer invalid.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testPassword456", user_type="teacher"
    )
    data = {
        "user": user.id,
        # 'content' is omitted
    }
    serializer = NotificationSerializer(data=data)
    assert not serializer.is_valid(), "Serializer should be invalid without content."
    assert "content" in serializer.errors, "Expected an error for missing 'content' field."


@pytest.mark.django_db
def test_notification_serializer_edge_case_invalid_user():
    """
    Edge case: Providing an invalid user ID should make the serializer invalid.
    """
    invalid_user_id = 99999  
    data = {
        "user": invalid_user_id,
        "content": "This is a test notification.",
    }
    serializer = NotificationSerializer(data=data)
    assert not serializer.is_valid(), "Serializer should be invalid with an invalid user ID."
    assert "user" in serializer.errors, "Expected an error for invalid 'user' field."