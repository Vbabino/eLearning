from .models import Course
from .serializers import CourseSerializer
from rest_framework import generics

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
