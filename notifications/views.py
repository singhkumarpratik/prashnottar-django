from django.views.generic import ListView
from django.shortcuts import render
from .models import Notification


class NotificationListView(ListView):
    model = Notification
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        context["notifications"] = notifications
        return context
        print(self.request.user.pk)


def show_notifications(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    return render(
        request, "notifications/notification.html", {"notification": notification}
    )
