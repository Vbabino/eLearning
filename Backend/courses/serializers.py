from rest_framework import serializers
from courses.models import Course, Enrollment, CourseMaterial

class CourseSerializer(serializers.ModelSerializer):
    # is_enrolled = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = "__all__"

    # def get_is_enrolled(self, obj):
    #     """Check if the authenticated user is enrolled in this course."""
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         return Enrollment.objects.filter(
    #             student=request.user, course=obj, is_active=True
    #         ).exists()
    #     return False


class EnrollmentSerializer(serializers.ModelSerializer):
    is_enrolled = serializers.SerializerMethodField()

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

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = "__all__"
