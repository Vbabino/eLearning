from django.db import models
from accounts.models import CustomUser
from courses.models import Course

class Feedback(models.Model):
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="feedbacks"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="feedbacks"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.email
