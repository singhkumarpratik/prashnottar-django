from django.urls import path
from . import views

app_name = "notifications"
urlpatterns = [
    path("all/", views.NotificationListView.as_view(), name="notifications_all",),
    path(
        "answers/",
        views.NotificationAnswerListView.as_view(),
        name="notifications_ans",
    ),
    path(
        "followed-questions/",
        views.NotificationFollowedQuestionsListView.as_view(),
        name="notifications_followed_questions",
    ),
    path(
        "<int:pk>", views.NotificationDetailView.as_view(), name="notification_detail",
    ),
    path("dismiss/all", views.dismiss_notification, name="dismiss_all_notification",),
    path("dismiss/<int:pk>", views.dismiss_notification, name="dismiss_notification",),
]
