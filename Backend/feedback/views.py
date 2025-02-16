from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer 
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStudent(BasePermission):
    message = "Only students can submit feedback."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "student"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.student == request.user


class FeedbackView(generics.ListCreateAPIView):
    """Students can submit feedback."""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStudent()]
        return [permissions.IsAuthenticated()]
