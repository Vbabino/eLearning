import re
from rest_framework import serializers
from courses.models import Course, Enrollment, CourseMaterial

class CourseSerializer(serializers.ModelSerializer):
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_enrolled(self, obj):
        """Check if the authenticated user is enrolled in this course."""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return Enrollment.objects.filter(
                student=request.user, course=obj, is_active=True
            ).exists()
        return False


class EnrollmentSerializer(serializers.ModelSerializer):
    is_enrolled = serializers.SerializerMethodField()
    student_details = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = "__all__"  

    def get_is_enrolled(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return Enrollment.objects.filter(
                student=request.user, course=obj.course, is_active=True
            ).exists()
        return False

    def get_student_details(self, obj):
        return {
            "email": obj.student.email,
            "first_name": obj.student.first_name,
            "last_name": obj.student.last_name,
        }

    def get_course_title(self, obj):
        """Return the title of the course the student is enrolled in."""
        return obj.course.title


class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = "__all__"

        def validate_file_name(self, value):
            """Ensure file_name only contains safe characters."""
            if not re.match(r'^[a-zA-Z0-9_\- ]+$', value):
                raise serializers.ValidationError(
                    "File name contains invalid characters. Only letters, numbers, spaces, underscores, and hyphens are allowed."
                )
            return value

        def validate_description(self, value):
            """Ensure description doesn't contain dangerous characters."""
            if not re.match(r'^[a-zA-Z0-9 .,!?()\'"-]+$', value):
                raise serializers.ValidationError(
                    "Description contains invalid characters."
                )
            return value

        def validate_file_min_length(self, value):
            """Ensure file_name is at least 5 characters long."""
            if not (5 <= len(value) <= 50):
                raise serializers.ValidationError("File name must be between 5 and 50 characters long.")
            return value

        def validate_description_min_length(self, value):   
            """Ensure description is between 5 and 100 characters."""
            if not (5 <= len(value) <= 100):
                raise serializers.ValidationError(
                    "Description must be between 5 and 100 characters long."
                )
            return value
