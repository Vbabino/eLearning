from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer
from user_permissions.user_permissions import IsStudent


class FeedbackView(generics.ListCreateAPIView):
    """Students can submit feedback."""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStudent()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
