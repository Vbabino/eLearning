from rest_framework.permissions import BasePermission, SAFE_METHODS
from courses.models import Course, Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()

class IsTeacher(BasePermission):
    message = (
        "Editing or deleting courses is restricted to the creator of the course only."
    )

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "teacher"

    def has_object_permission(self, request, view, obj):  # -> Any | Literal[True]:
        if request.method in SAFE_METHODS:
            return True

        # If the object is a Course, check obj.teacher
        if isinstance(obj, Course):
            return obj.teacher == request.user

        # If the object is an Enrollment, check obj.course.teacher
        if isinstance(obj, Enrollment):
            return obj.course.teacher == request.user

        return False


class IsStudent(BasePermission):
    message = "Only students can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "student"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.student == request.user
