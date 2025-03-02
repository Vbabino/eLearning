from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.timezone import now
from notifications.models import Notification  
from accounts.models import CustomUser

@shared_task
def notify_teacher_on_enrollment(course_id, student_name, teacher_id):
    """Notifies the teacher when a student enrolls."""
    message = f"{student_name} has enrolled in your course."

    # Save notification to the database
    teacher = CustomUser.objects.get(id=teacher_id)
    Notification.objects.create(user=teacher, content=message, created_at=now())

    # Send WebSocket notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{teacher_id}",
        {"type": "send_notification", "message": message},
    )


@shared_task
def notify_students_on_material_upload(course_id, teacher_name, student_ids):
    """Notifies students when new material is uploaded."""
    message = f"New material has been uploaded by {teacher_name}."

    # Send WebSocket notifications
    channel_layer = get_channel_layer()
    for student_id in student_ids:
        # Save notification in the database
        student = CustomUser.objects.get(id=student_id)
        Notification.objects.create(user=student, content=message, created_at=now())

        # Send WebSocket notification
        async_to_sync(channel_layer.group_send)(
            f"notifications_{student_id}",
            {"type": "send_notification", "message": message},
        )


@shared_task
def notify_student_on_profile_update(student_id):
    try:
        student = CustomUser.objects.get(id=student_id)
        Notification.objects.create(
            user=student, content="Your profile has been updated.", created_at=now()
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{student_id}",
            {"type": "send_notification", "message": "Your profile has been updated."},
        )
    except CustomUser.DoesNotExist:
        print(f"User {student_id} not found. Skipping notification.")
