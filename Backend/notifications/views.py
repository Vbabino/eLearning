# from rest_framework import generics, permissions
# from .models import StatusUpdate
# from .serializers import StatusUpdateSerializer
# from rest_framework.permissions import BasePermission, SAFE_METHODS


# class IsStudent(BasePermission):
#     message = "Only students can submit feedback."

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.user_type == "student"

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         return obj.student == request.user

# class StatusUpdateView(generics.ListCreateAPIView):
#     """Students can submit status updates to their home page."""
#     queryset = StatusUpdate.objects.all()
#     serializer_class = StatusUpdateSerializer

#     def get_permissions(self):
#         if self.request.method == "POST":
#             return [IsStudent()]
#         return [permissions.IsAuthenticated()]