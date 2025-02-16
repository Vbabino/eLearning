from django.urls import path
from . import views  

urlpatterns = [
    path("list/", views.CourseListView.as_view(), name="course-list"),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),
    path("<int:pk>/enroll/", views.CourseEnrollView.as_view(), name="course-enroll"),
    path("teacher/students/", views.TeacherEnrolledStudentsView.as_view(), name="teacher-students"),
]
