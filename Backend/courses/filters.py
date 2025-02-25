import django_filters
from courses.models import Course

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            "title": ["iexact", "icontains"],
            "description": ["iexact", "icontains"],
        }
        exclude = ["created_at", "updated_at"]