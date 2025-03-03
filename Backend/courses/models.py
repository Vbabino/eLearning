from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinLengthValidator


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="courses"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseMaterial(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="materials"
    )
    file = models.FileField(upload_to="materials/", null=True, blank=True)
    file_name = models.CharField(
        max_length=255,
        default="Untitled",
        null=False,
        blank=False,
        validators=[MinLengthValidator(5)],
    )
    description = models.TextField(
        validators=[MinLengthValidator(5)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Enrollment(models.Model):
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrolled_students"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
