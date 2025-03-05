import uuid
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import CustomUser
from accounts.serializers import UserProfilePhotoSerializer
from io import BytesIO
from PIL import Image
from accounts.utils import generate_valid_image


@pytest.mark.django_db
def test_user_profile_photo_serializer_positive():
    """
    Positive test: Serializer is valid when using a valid PNG image under 5MB.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testpass", user_type="student"
    )
    valid_image = generate_valid_image()

    data = {"photo": valid_image}
    serializer = UserProfilePhotoSerializer(instance=user, data=data, partial=True)
    assert (
        serializer.is_valid()
    ), f"Serializer should be valid. Errors: {serializer.errors}"


@pytest.mark.django_db
def test_user_profile_photo_serializer_negative_invalid_extension():
    """
    Negative test: Serializer should fail when the file extension is not allowed.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testpass", user_type="teacher"
    )
    invalid_image = SimpleUploadedFile(
        name="test_file.gif",
        content=b"GIF89a",  
        content_type="image/gif",
    )

    data = {"photo": invalid_image}
    serializer = UserProfilePhotoSerializer(instance=user, data=data, partial=True)
    assert not serializer.is_valid(), "Serializer should be invalid for .gif extension."
    assert "photo" in serializer.errors, "Expected error on 'photo' field."


@pytest.mark.django_db
def test_user_profile_photo_serializer_edge_case_oversized():
    """
    Edge case test: Serializer should fail when file size exceeds 5MB.
    """
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com", password="testpass", user_type="student"
    )
    # Create a ~6MB dummy file
    oversized_content = b"x" * (6 * 1024 * 1024)
    oversized_image = SimpleUploadedFile(
        name="large.png",
        content=oversized_content,
        content_type="image/png",
    )

    data = {"photo": oversized_image}
    serializer = UserProfilePhotoSerializer(instance=user, data=data, partial=True)
    assert not serializer.is_valid(), "Serializer should be invalid for files over 5MB."
    assert "photo" in serializer.errors, "Expected error on 'photo' field."
