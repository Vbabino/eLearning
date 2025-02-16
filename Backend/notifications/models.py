from django.db import models
from accounts.models import CustomUser


class StatusUpdate(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="status_updates"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
