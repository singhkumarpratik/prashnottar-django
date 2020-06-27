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
    template_name = "notifications/notification_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(
            to_user=self.request.user.pk, is_answer=True
        ).order_by("-created_date")
        context["notifications"] = notifications
        return context


class NotificationFollowedQuestionsListView(ListView):
    model = Notification
    template_name = "notifications/notification_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(
            to_user=self.request.user.pk, is_followed_question=True
        ).order_by("-created_date")
        context["notifications"] = notifications
        return context


def dismiss_notification(request, pk=None):
    if request.user.is_authenticated:
        try:
            if pk is None:
                """dismiss all"""
                Notification.objects.filter(to_user=request.user.pk).delete()
                return JsonResponse({"dismiss_all": True, "success": True})
            else:
                Notification.objects.get(pk=pk).delete()
                return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False})
