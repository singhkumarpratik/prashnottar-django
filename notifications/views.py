from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification


class NotificationListView(ListView):
    model = Notification

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        context["notifications"] = notifications
        return context


class NotificationDetailView(DetailView):
    model = Notification
    queryset = Notification.objects.all()
    # context_object_name = "notification"

    def get_context_data(self, **kwargs):
        context = super(NotificationDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        obj.is_seen = True
        obj.save()
        from_user = obj.from_user
        question = obj.question
        ans = question.answer_set.get(user=from_user.pk)
        context["from_user"] = from_user
        context["question"] = question
        context["ans"] = ans
        return context
        print(from_user, question, ans)


def show_notifications(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    return render(
        request, "notifications/notification.html", {"notification": notification}
    )


def mark_as_read(request):
    if request.user.is_authenticated:
        if request.is_ajax and request.method == "GET":
            # pk = request.GET.get("pk")
            # notification = Notification.objects.get(pk=pk)
            # notification.is_seen
            # return JsonResponse({"is_seen": notification.is_seen})
            pass
