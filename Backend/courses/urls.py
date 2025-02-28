from django.urls import path
from . import views

urlpatterns = [
    # Manage view courses
    path("list/", views.CourseListView.as_view(), name="course-list"),
    path(
        "<int:pk>/", views.CourseDetailViewForStudents.as_view(), name="course-detail"
    ),
    path("course/search/", views.SearchCourseView.as_view(), name="course-search"),
    path(
        "list/students/",
        views.CourseListViewForStudents.as_view(),
        name="course-list-students",
    ),
    # Manage courses
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),
    path("<int:pk>/enroll/", views.CourseEnrollView.as_view(), name="course-enroll"),
    # Course materials
    path(
        "<int:pk>/materials/",
        views.CourseMaterialUploadView.as_view(),
        name="course-materials",
    ),
    path(
        "materials/<int:pk>/",
        views.CourseMaterialListView.as_view(),
        name="course-materials",
    ),
    # Enrrolled students
    path(
        "teacher/students/",
        views.TeacherEnrolledStudentsView.as_view(),
        name="teacher-students",
    ),
    path(
        "<int:course_id>/remove_student/<int:pk>/",
        views.RemoveStudentView.as_view(),
        name="remove-student",
    ),
    path(
        "<int:course_id>/unblock_student/<int:pk>/",
        views.UnblockStudentView.as_view(),
        name="unblock-student",
    ),
]
