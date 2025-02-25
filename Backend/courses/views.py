from .models import Course, Enrollment, CourseMaterial
from .serializers import (
    CourseSerializer,
    EnrollmentSerializer,
    CourseMaterialSerializer,
)
from rest_framework import generics, permissions, status, serializers
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from notifications.tasks import (
    notify_teacher_on_enrollment,
    notify_students_on_material_upload,
)

from user_permissions.user_permissions import IsTeacher, IsStudent


class CourseListView(generics.ListCreateAPIView):
    """Teachers can create courses, students can only view courses."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CourseDetailViewForStudents(generics.RetrieveAPIView):
    """Students can view details of a course."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


# TODO: Fix the issue with the course list view
# class CourseDetailView(generics.RetrieveAPIView):
#     """Teachers and Students can view details of a course.

#     This view allows authenticated users to retrieve details of a specific course.
#     The view uses the `CourseSerializer` to serialize the course data and ensures
#     that only authenticated users can access it by using the `IsAuthenticated`
#     permission class.

#     The `get_queryset` method customizes the queryset based on the type of user:
#     - If the user is a teacher, it returns all courses taught by that teacher.
#     - If the user is a student, it returns only the courses in which the student
#       is actively enrolled.

#     Methods:
#     - get_queryset(self): Returns a queryset of courses based on the user's type
#       and enrollment status.
#     """

#     serializer_class = CourseSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         """Ensure only active students can access course details."""
#         user = self.request.user
#         if user.user_type == "teacher":
#             return Course.objects.all().filter(teacher=user)
#         return Course.objects.filter(
#             enrollments__student=user, enrollments__is_active=True
#         )


class CourseUpdateView(generics.RetrieveUpdateAPIView):
    """Only the teacher who created the course can update it."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacher]


class CourseDeleteView(generics.DestroyAPIView):
    """Only the teacher who created the course can delete it."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacher]


class CourseEnrollView(generics.CreateAPIView):
    """Students can enroll in a course."""

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        student = self.request.user
        course_id = self.kwargs.get("pk")
        if not course_id:
            raise serializers.ValidationError("Course ID is required.")
        course = Course.objects.get(id=course_id)

        # Check if already enrolled
        if Enrollment.objects.filter(
            student=student, course=course, is_active=True
        ).exists():
            raise serializers.ValidationError(
                "You are already enrolled in this course."
            )

        enrollment = serializer.save(student=student, course=course)

        notify_teacher_on_enrollment.delay(
            course_id=enrollment.course.id,
            student_name=student.email,
            teacher_id=enrollment.course.teacher.id,
        )

    def get_serializer_context(self):
        """Pass request context to serializer so is_enrolled can be computed."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class CourseMaterialUploadView(generics.CreateAPIView):
    """Teachers can upload course material."""

    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    permission_classes = [IsTeacher]

    def perform_create(self, serializer):
        """ Ensure course exists and notify students."""
        material = serializer.save()
        
        enrolled_students = Enrollment.objects.filter(
            course=material.course
        ).values_list("student__id", flat=True)

        notify_students_on_material_upload.delay(
            course_id=material.course.id,
            teacher_name=self.request.user.email,
            student_ids=list(enrolled_students),
        )


class TeacherEnrolledStudentsView(generics.ListAPIView):
    """Teachers can view students enrolled in their course."""

    def get_queryset(self):
        """Ensure only authenticated teachers can fetch enrolled students."""
        if getattr(self, "swagger_fake_view", False):
            return Enrollment.objects.none()

        if (
            self.request.user.is_authenticated
            and self.request.user.user_type == "teacher"
        ):
            return Enrollment.objects.filter(course__teacher=self.request.user)
        return Enrollment.objects.none()

    @extend_schema(
        description="Teachers can view students enrolled in their courses.",
        responses={200: EnrollmentSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RemoveStudentView(generics.UpdateAPIView):
    """Teachers can remove students from their course."""

    serializer_class = EnrollmentSerializer
    permission_classes = [IsTeacher]
    lookup_field = "pk"

    def get_queryset(self):
        """Ensure only teachers can remove students from their own courses."""
        return Enrollment.objects.filter(course__teacher=self.request.user)

    def update(self, request, *args, **kwargs):
        """Set `is_active` to False."""
        enrollment = self.get_object()

        if enrollment.course.teacher != request.user:
            return Response(
                {"error": "You can only remove students from your own courses."},
                status=403,
            )

        enrollment.is_active = False
        enrollment.save()
        return Response(
            {"message": "Student removed from course."}, status=status.HTTP_200_OK
        )


class UnblockStudentView(generics.UpdateAPIView):
    """Teachers can unblock students from their course."""

    serializer_class = EnrollmentSerializer
    permission_classes = [IsTeacher]
    lookup_field = "pk"

    def get_queryset(self):
        """Ensure only teachers can unblock students from their own courses."""
        return Enrollment.objects.filter(course__teacher=self.request.user)

    def update(self, request, *args, **kwargs):
        """Set `is_active` to True."""
        enrollment = self.get_object()

        if enrollment.course.teacher != request.user:
            return Response(
                {"error": "You can only unblock students from your own courses."},
                status=403,
            )

        enrollment.is_active = True
        enrollment.save()
        return Response(
            {"message": "Student unblocked from course."}, status=status.HTTP_200_OK
        )
