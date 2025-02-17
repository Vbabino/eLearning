from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task

def notify_teacher_on_enrollment(course_id, student_name, teacher_id):
    """Notifies the teacher when a student enrolls."""
    message = f"{student_name} has enrolled in your course."

    # Send WebSocket notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{teacher_id}",
        {"type": "send_notification", "message": message},
    )


@shared_task
def notify_students_on_material_upload(course_id, teacher_name, student_ids):
    """ Notifies students when new material is uploaded."""
    message = f"New material has been uploaded by {teacher_name}."

    # Send WebSocket notifications
    channel_layer = get_channel_layer()
    for student_id in student_ids:
        async_to_sync(channel_layer.group_send)(
            f"notifications_{student_id}",
            {"type": "send_notification", "message": message},
        )
