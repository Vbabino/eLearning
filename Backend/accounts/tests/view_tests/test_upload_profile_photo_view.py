import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import CustomUser
from io import BytesIO
from PIL import Image
from accounts.utils import generate_valid_image


@pytest.mark.django_db
def test_upload_profile_photo_view_positive():
    """
    Positive test: A valid .png photo under 5MB should successfully upload.
    """
    client = APIClient()

    # Create and authenticate a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="validPassword123",
        user_type="student",
    )
    client.force_authenticate(user=user)

    url = reverse("upload_profile_photo", kwargs={"pk": user.id})

    # Use the generated valid image
    valid_image = generate_valid_image()
    data = {
        "photo": valid_image,
    }

    response = client.put(url, data=data, format="multipart")
    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}, Response: {response.content}"
    )
    user.refresh_from_db()
    assert user.photo, "User photo field should be set."


@pytest.mark.django_db
def test_upload_profile_photo_view_negative_invalid_extension():
    """
    Negative test: Uploading an unsupported file extension (e.g., .gif) should fail.
    """
    client = APIClient()

    # Create and authenticate a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword456",
        user_type="teacher",
    )
    client.force_authenticate(user=user)

    url = reverse("upload_profile_photo", kwargs={"pk": user.id})

    # Mock a .gif file which is not supported
    invalid_image = SimpleUploadedFile(
        name="invalid_file.gif",
        content=b"GIF89a",
        content_type="image/gif",
    )
    data = {"photo": invalid_image}
    response = client.put(url, data=data, format="multipart")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.content}"
    )
    assert "Only JPG, JPEG, and PNG files are allowed." in str(response.content), (
        "Expected error message about invalid file extension."
    )


@pytest.mark.django_db
def test_upload_profile_photo_view_edge_case_exceed_size_limit():
    """
    Edge case test: A file exceeding the 5MB limit should fail.
    """
    client = APIClient()

    # Create and authenticate a user
    user = CustomUser.objects.create_user(
        email=f"{uuid.uuid4()}@example.com",
        password="testPassword789",
        user_type="student",
    )
    client.force_authenticate(user=user)

    url = reverse("upload_profile_photo", kwargs={"pk": user.id})

    # Create a ~6MB dummy file to exceed the 5MB limit
    oversized_content = b"x" * (6 * 1024 * 1024)
    oversized_image = SimpleUploadedFile(
        name="large.png",
        content=oversized_content,
        content_type="image/png",
    )
    data = {"photo": oversized_image}
    response = client.patch(url, data=data, format="multipart")

    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}, Response: {response.content}"
    )
    assert "Profile photo size exceeds 5MB." in str(response.content), (
        "Expected error message about exceeding file size."
    )
