import math
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, Http404
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from comments.models import MyComment
from .models import *
from .forms import *
from .get_topics import *
from users.models import User, Follow
from notifications.models import Notification


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
                if len(related_questions) != 8 and match not in related_questions:
                    related_questions.append(match)
                else:
                    max_matches = True
                    break
            if max_matches:
                break
        is_following = FollowQuestion.objects.filter(
            user=self.request.user.pk, question=self.get_object()
        )
        try:
            """this is in try/except block otherwise it'll throw error when a user who isn't logged in visits a question detail page"""
            is_answered = self.get_object().answer_set.filter(user=self.request.user)
            context["is_answered"] = is_answered
        except:
            pass
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
        if not question.is_anonymous:
            followers = Follow.objects.filter(to_user=self.request.user)
            for follower in followers:
                Notification.objects.create(
                    from_user=self.request.user,
                    to_user=follower.from_user,
                    msg=f"{self.request.user.first_name} {self.request.user.last_name} asked a question: {question.title}",
                    question=question,
                    is_following_user_questions=True,
                )
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
        if not answer.is_anonymous:
            followers = Follow.objects.filter(to_user=self.request.user)
            for follower in followers:
                if follower.from_user != question.user:
                    Notification.objects.create(
                        from_user=self.request.user,
                        to_user=follower.from_user,
                        msg=f"{self.request.user.first_name} {self.request.user.last_name} answered a question: {question.title}",
                        question=question,
                        is_following_user_answers=True,
                    )
        return redirect(reverse("qnA:question_detail", kwargs={"slug": question_slug}))

    def get_context_data(self, **kwargs):
        context = super(AnswerView, self).get_context_data(**kwargs)
        question_slug = self.kwargs.get("slug")
        question = Question.objects.get(slug=question_slug)
        context["question"] = question
        return context

    def dispatch(self, request, *args, **kwargs):
        """redirect to edit answer url if answer of the user already exists"""
        question_slug = self.kwargs.get("slug")
        question = Question.objects.get(slug=question_slug)
        try:
            Answer.objects.get(question=question, user=request.user)
            return redirect(reverse("qnA:edit", kwargs={"slug": question_slug}))
        except:
            pass
        return super(AnswerView, self).dispatch(request, *args, **kwargs)


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
        try:
            ans = question.answer_set.get(user=self.request.user)
            return ans
        except:
            raise Http404

    def get_success_url(self, **kwargs):
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
    login_url = "/users/login/"

    def get_object(self, queryset=None):
        question = super().get_object(queryset=queryset)
        try:
            ans = question.answer_set.get(user=self.request.user)
            return ans
        except:
            raise Http404

    def get_success_url(self, **kwargs):
        return reverse_lazy("qnA:question_detail", args=(self.object.question.slug,))


class RequestAnswerListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "qnA/answer_request.html"
    login_url = "/users/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_slug = self.kwargs["slug"]
        question = Question.objects.get(slug=question_slug)
        try:
            searched_user = self.request.GET.get("user")
            try:
                first_name, *_, last_name = searched_user.split()
                users_list = User.objects.filter(
                    first_name__contains=first_name, last_name__contains=last_name
                )
            except:
                """ only one name entered """
                users_list = User.objects.filter(
                    Q(first_name__contains=searched_user)
                    | Q(last_name__contains=searched_user)
                )
            user_l = {}
            for user in users_list:
                is_requested_question = Notification.objects.filter(
                    from_user=self.request.user.pk,
                    to_user=user.pk,
                    question=question,
                    is_requested_question=True,
                )
                user_l[user] = is_requested_question

            context["user_l"] = user_l
        except:
            answer_users = []
            for answer in question.answer_set.all():
                answer_users.append(answer.user)
            question_topics = question.topics.all()
            suggested_users = {}
            for topic in question_topics:
                """find similar questions"""
                matches = Question.objects.filter(title__icontains=topic).exclude(
                    slug=question_slug
                )[:10]
                for match in matches:
                    """for each similar questions, get those question's answers's users and add them to suggested_user list"""
                    answers = match.answer_set.all().order_by("-vote_score")
                    for answer in answers:
                        if (
                            answer.user not in answer_users
                            and answer.user != question.user
                        ):
                            is_requested_question = Notification.objects.filter(
                                from_user=self.request.user.pk,
                                to_user=answer.user.pk,
                                question=question,
                                is_requested_question=True,
                            )
                            """checking if the request.user had already requested the answer"""
                            is_requested_question = (
                                True if is_requested_question else False
                            )
                            suggested_users[answer.user] = is_requested_question
            context["suggested_users"] = suggested_users
        context["question"] = question
        return context


def request_answer(request, question_pk, user_pk):
    if request.user.is_authenticated:
        from_user = request.user
        to_user = User.objects.get(pk=user_pk)
        try:
            question = Question.objects.get(pk=question_pk)
            try:
                """checking if notification is already sent"""
                Notification.objects.get(
                    from_user=from_user,
                    to_user=to_user,
                    question=question,
                    is_requested_question=True,
                )
                return redirect("qnA:home")
            except:
                msg = f"{from_user.first_name} {from_user.last_name} requested you to answer the question: {question}"
                Notification.objects.create(
                    from_user=from_user,
                    to_user=to_user,
                    msg=msg,
                    question=question,
                    is_requested_question=True,
                )
                return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False})
    return redirect("users:login")


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
