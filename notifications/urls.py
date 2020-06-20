from django.urls import path
from . import views

app_name = "notifications"
urlpatterns = [
    path("show/all", views.NotificationListView.as_view(), name="notifications",),
    path("show/<int:notification_id>", views.show_notifications, name="notifications",),
]
