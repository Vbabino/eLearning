from django.urls import path
from . import views  

urlpatterns = [
    path("list/", views.CourseListView.as_view(), name="course-list"),
]
