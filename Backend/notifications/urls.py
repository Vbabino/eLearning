from django.urls import path
from . import views

urlpatterns = [
    # path("status_updates/", views.StatusUpdateView.as_view(), name="status_updates"),
    path("notifications/", views.NotificationListView.as_view(), name="notification-list"),
]
