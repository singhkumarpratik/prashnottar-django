from django.shortcuts import render
from django.views.generic import ListView
from .models import Question, Answer


class QnaListView(ListView):
    model = Question
    # queryset = model.objects.get(pk=self.pk)
    # print(queryset)
    template_name = "qnA/qnA_list.html"

    def get_context_data(self, **kwargs):
        context = super(QnaListView, self).get_context_data(**kwargs)
        questions = Question.objects.all()
        context["questions"] = questions
        return context


""" from django.shortcuts import render
from django.views.generic import TemplateView
from . import models


class QnaListView(TemplateView):
    template_name = "qnA/qnA_list.html"

    def get_context_data(self, **kwargs):
        context = super(QnaListView, self).get_context_data(**kwargs)
        questions = models.Question.objects.all()
        for i in questions:
            latest_ans = models.Answer.objects.filter(question=i).latest("updated_date")
            print(latest_ans)
        context["questions"] = questions
        return context
 """
