import math
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, FormView
from django.utils import timezone
from comments.models import MyComment
from .models import Question, Answer, Topic
from .forms import *
from .get_topics import *


class QnaListView(ListView):
    model = Question
    template_name = "qnA/qnA_list.html"

    def get_context_data(self, **kwargs):
        context = super(QnaListView, self).get_context_data(**kwargs)
        questions = Question.objects.all()
        for question in questions:
            order = math.log(max(abs(question.vote_score), 1), 10)
            if question.vote_score > 0:
                sign = 1
            elif question.vote_score < 0:
                sign = -1
            else:
                sign = 0
            seconds = (question.created_date).timestamp() - 1134028003
            question.rank = round(sign * order + seconds / 10800, 7)
            print(seconds, question.rank, question.title)
        sorted_submissions = sorted(questions, key=lambda x: x.rank, reverse=True)
        context["questions"] = sorted_submissions
        return context


class QuestionDetailView(DetailView):
    queryset = Question.objects.all()


class AskQuestionView(FormView):
    template_name = "qnA/ask_question.html"
    form_class = QuestionForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        question = form.save(commit=False)
        question.user = self.request.user
        question_topics = get_topics(question.title)
        question.save()
        for topic in question_topics:
            if not Topic.objects.filter(topic=topic).exists():
                Topic.objects.create(topic=topic)
            question.topics.add(Topic.objects.get(topic=topic))
        return redirect(reverse("qnA:question_detail", kwargs={"slug": question.slug}))


class AnswerView(FormView):
    template_name = "qnA/ask_question.html"
    form_class = AnswerForm

    def form_valid(self, form):
        question_slug = self.kwargs.get("slug")
        question = Question.objects.get(slug=question_slug)
        answer = form.save(commit=False)
        answer.user = self.request.user
        answer.question = question
        answer.save()
        return redirect(reverse("qnA:question_detail", kwargs={"slug": question_slug}))


def vote(request, question_id, slug=None):
    if request.user.is_authenticated:
        if request.is_ajax and request.method == "GET":
            is_question_detail = False
            if slug is not None:
                is_question_detail = True
                if request.GET.get("is_comment") == "True":
                    question = MyComment.objects.get(pk=question_id)
                    print(question)
                else:
                    question = Answer.objects.get(pk=question_id)
            else:
                question = Question.objects.get(pk=question_id)
            user_votes_up = question.votes.user_ids(0)
            user_votes_down = question.votes.user_ids(1)
            check = {"user_id": request.user.id}
            if request.GET.get("up"):
                if check in user_votes_up.values("user_id"):
                    question.votes.delete(request.user.id)
                else:
                    question.votes.up(request.user.id)
            if request.GET.get("down"):
                if check in user_votes_down.values("user_id"):
                    question.votes.delete(request.user.id)
                else:
                    question.votes.down(request.user.id)
            if request.GET.get("status"):
                has_upvoted = question.votes.exists(request.user.id, action=0)
                has_downvoted = question.votes.exists(request.user.id, action=1)
                return JsonResponse(
                    {
                        "has_upvoted": has_upvoted,
                        "has_downvoted": has_downvoted,
                        "is_question_detail": is_question_detail,
                    }
                )
            if slug is not None:
                if request.GET.get("is_comment") == "True":
                    question = MyComment.objects.get(pk=question_id)
                    print(question)
                else:
                    question = Answer.objects.get(pk=question_id)
            else:
                question = Question.objects.get(pk=question_id)
            has_upvoted = question.votes.exists(request.user.id, action=0)
            has_downvoted = question.votes.exists(request.user.id, action=1)
            return JsonResponse(
                {
                    "valid": True,
                    "data": {
                        "score": question.vote_score,
                        "has_upvoted": has_upvoted,
                        "has_downvoted": has_downvoted,
                        "is_question_detail": is_question_detail,
                    },
                },
                status=200,
            )
    else:
        return redirect("users:login")
