from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification


class NotificationListView(ListView):
    model = Notification

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(
            to_user=self.request.user.pk
        ).order_by("-created_date")
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


class NotificationAnswerListView(ListView):
    model = Notification

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(
            to_user=self.request.user.pk, is_answer=True
        ).order_by("-created_date")
        context["notifications"] = notifications
        return context


class NotificationFollowedQuestionsListView(ListView):
    model = Notification

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(
            to_user=self.request.user.pk, is_followed_question=True
        ).order_by("-created_date")
        context["notifications"] = notifications
        return context


def show_notifications(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    return render(
        request, "notifications/notification.html", {"notification": notification}
    )
