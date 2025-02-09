from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

USER_TYPES = [("student", "Student"), ("teacher", "Teacher")]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    real_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )


class StatusUpdate(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="status_updates"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
