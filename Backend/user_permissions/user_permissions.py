from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacher(BasePermission):
    message = (
        "Editing or deleting courses is restricted to the creator of the course only."
    )

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "teacher"

    def has_object_permission(self, request, view, obj):  # -> Any | Literal[True]:
        if request.method in SAFE_METHODS:
            return True

        return obj.course.teacher == request.user


class IsStudent(BasePermission):
    message = "Only students can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "student"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.student == request.user
