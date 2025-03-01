from rest_framework import serializers
from courses.models import Course, Enrollment, CourseMaterial
from feedback.models import Feedback

class CourseSerializer(serializers.ModelSerializer):
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_enrolled(self, obj):
        """Check if the authenticated user is enrolled in this course."""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            feedback = Feedback.objects.filter(course=obj, student=request.user).first()
            if feedback:
                return feedback.id
        return None


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
