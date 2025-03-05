import os
from django.core.mail import send_mail
from django.conf import settings
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def generate_valid_image():
    """Create an in-memory image file."""
    image_io = BytesIO()
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Red square
    image.save(image_io, format="PNG")
    image_io.seek(0)
    return SimpleUploadedFile(
        "valid_image.png", image_io.getvalue(), content_type="image/png"
    )


def send_otp_email(user, otp):
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp}"

    email_path = os.path.join(settings.EMAIL_FILE_PATH)
    os.makedirs(email_path, exist_ok=True)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_approval_email(user):
    subject = "Your Account Has Been Approved"
    message = "Congratulations! Your account has been approved."

    email_path = os.path.join(settings.EMAIL_FILE_PATH)
    os.makedirs(email_path, exist_ok=True)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
