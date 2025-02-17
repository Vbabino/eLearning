from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from notifications.tasks import notify_teacher_on_enrollment, notify_students_on_material_upload


class IsTeacher(BasePermission):
    message = "Editing or deleting courses is restricted to the creator of the course only."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "teacher"

    def has_object_permission(self, request, view, obj):  # -> Any | Literal[True]:
        if request.method in SAFE_METHODS:
            return True

        return obj.teacher == request.user


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


class CourseDetailView(generics.RetrieveAPIView):
    """Teachers and Students can view details of a course."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        enrollment = serializer.save(student=self.request.user)
        notify_teacher_on_enrollment.delay(
            course_id=enrollment.course.id,
            student_name=self.request.user.username,
            teacher_id=enrollment.course.teacher.id,
        )

class CourseMaterialUploadView(generics.CreateAPIView):
    """Teachers can upload course material."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacher]

    def perform_create(self, serializer):
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

    serializer_class = EnrollmentSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Enrollment.objects.filter(course__teacher=self.request.user)
