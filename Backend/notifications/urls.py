from django.urls import path
from . import views

urlpatterns = [
    path("notifications/", views.NotificationListView.as_view(), name="notification-list"),
    path("notifications/<int:pk>/", views.NotificationDeleteView.as_view(), name="notification-delete"),
]
