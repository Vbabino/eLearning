import os
from django.core.mail import send_mail
from django.conf import settings

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
