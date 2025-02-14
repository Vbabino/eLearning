from django.urls import path, include

urlpatterns = [
    path("auth/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("feedback/", include("feedback.urls")),
    # path("chat/", include("chat.urls")),
    # path("whiteboard/", include("whiteboard.urls")),
    # path("notifications/", include("notifications.urls")),
]
