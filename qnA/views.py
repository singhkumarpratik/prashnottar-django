from django.shortcuts import render
from django.views.generic import ListView, DetailView
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


class QuestionDetailView(DetailView):
    queryset = Question.objects.all()
