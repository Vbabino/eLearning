from django.db import models
from accounts.models import CustomUser


class StatusUpdate(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="status_updates"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.content}"