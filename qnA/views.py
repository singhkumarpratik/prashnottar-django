import math
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.models import MyComment
from .models import *
from .forms import *
from .get_topics import *


class QnaListView(ListView):
    model = Question
    template_name = "qnA/qnA_list.html"
    paginate_by = 10
    context_object_name = "questions"

    def get_queryset(self):
        try:
            question = self.request.GET.get("question")
            questions = Question.objects.filter(title__icontains=question)
        except:
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
        sorted_submissions = sorted(questions, key=lambda x: x.rank, reverse=True)
        paginator = Paginator(sorted_submissions, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            pagin = paginator.page(page)
        except PageNotAnInteger:
            pagin = paginator.page(1)
        except EmptyPage:
            pagin = paginator.page(paginator.num_pages)
        return sorted_submissions


class QuestionDetailView(DetailView):
    queryset = Question.objects.all()

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        topics = self.get_object().topics.all()
        related_questions = []
        max_matches = False
        for topic in topics:
            matches = Question.objects.filter(title__icontains=topic).exclude(
                pk=self.get_object().pk
            )
            for match in matches:
                if len(related_questions) != 8:
                    related_questions.append(match)
                else:
                    max_matches = True
                    break
            if max_matches:
                break
        is_following = FollowQuestion.objects.filter(
            user=self.request.user.pk, question=self.get_object()
        )
        is_answered = self.get_object().answer_set.filter(user=self.request.user)
        context["is_answered"] = is_answered
        context["is_following"] = is_following
        context["related_questions"] = related_questions
        return context


class AskQuestionView(LoginRequiredMixin, FormView):
    login_url = "/users/login/"
    template_name = "qnA/qnA.html"
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


class AnswerView(LoginRequiredMixin, FormView):
    login_url = "/users/login/"
    template_name = "qnA/qnA.html"
    form_class = AnswerForm

    def form_valid(self, form):
        question_slug = self.kwargs.get("slug")
        question = Question.objects.get(slug=question_slug)
        answer = form.save(commit=False)
        answer.user = self.request.user
        answer.question = question
        answer.save()
        return redirect(reverse("qnA:question_detail", kwargs={"slug": question_slug}))

    def get_context_data(self, **kwargs):
        context = super(AnswerView, self).get_context_data(**kwargs)
        question_slug = self.kwargs.get("slug")
        question = Question.objects.get(slug=question_slug)
        context["question"] = question
        return context


class AnswerDetailView(DetailView):
    queryset = Question.objects.all()
    template_name = "qnA/answer_detail.html"

    def get_context_data(self, **kwargs):
        context = super(AnswerDetailView, self).get_context_data(**kwargs)
        question_pk = self.kwargs.get("question_pk")
        user_pk = self.kwargs.get("user_pk")
        question = Question.objects.get(pk=question_pk)
        user_answer = question.answer_set.get(user=user_pk)
        context["user_answer"] = user_answer
        return context


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "qnA/qnA.html"
    model = Question
    form_class = AnswerForm
    login_url = "/users/login/"

    def get_object(self, queryset=None):
        question = super().get_object(queryset=queryset)
        ans = question.answer_set.get(user=self.request.user)
        return ans

    def get_success_url(self, **kwargs):
        print(self.object.question.slug)
        return reverse_lazy(
            "qnA:answer_detail",
            args=(
                self.object.question.slug,
                self.object.user.slug,
                self.object.question.pk,
                self.object.user.pk,
            ),
        )


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Question

    def get_object(self, queryset=None):
        question = super().get_object(queryset=queryset)
        ans = question.answer_set.get(user=self.request.user)
        return ans

    def get_success_url(self, **kwargs):
        print(self.object.question.slug)
        return reverse_lazy("qnA:question_detail", args=(self.object.question.slug,))


def follow_question(request, question_slug):
    if request.user.is_authenticated:
        user = request.user
        question_slug = question_slug
        question = Question.objects.get(slug=question_slug)
        if question.user != user:
            """
            users who created the question will automatically be notified when a new answer comes. Therefore,
            this check is done to prevent them from getting notification twice.
            """
            try:
                # FollowQuestion.objects.get(question=question, user=user)
                FollowQuestion.objects.get(question=question, user=user).delete()
                is_following = False
            except:
                FollowQuestion.objects.create(question=question, user=user)
                is_following = True
            return JsonResponse(
                {"is_following": is_following, "is_question_follow": True}
            )
    return redirect("users:login")


def vote(request, question_id, slug=None):
    if request.user.is_authenticated:
        if request.is_ajax and request.method == "GET":
            is_question_detail = False
            if slug is not None:
                is_question_detail = True
                if request.GET.get("is_comment") == "True":
                    question = MyComment.objects.get(pk=question_id)
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
