from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, FormView
from comments.models import MyComment
from .models import Question, Answer, Topic
from .forms import QuestionForm
from .get_topics import *


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


def vote(request, question_id, slug=None):
    # check if user is logged in. If not redirect to login page
    if request.user.is_authenticated:
        if request.is_ajax and request.method == "GET":
            is_question_detail = False
            # if a specific question's page is opened
            if slug is not None:
                is_question_detail = True
                # print(request.GET.get("is_comment"), "hii")
                if request.GET.get("is_comment") == "True":
                    question = MyComment.objects.get(pk=question_id)
                    print(question)
                else:
                    question = Answer.objects.get(pk=question_id)
            else:
                question = Question.objects.get(pk=question_id)
            # 0 is upvote, 1 is downvote
            user_votes_up = question.votes.user_ids(0)
            user_votes_down = question.votes.user_ids(1)
            check = {"user_id": request.user.id}
            # get the value passed from the form
            if request.GET.get("up"):
                # check if user has already upvoted, if yes, remove user's upvote
                if check in user_votes_up.values("user_id"):
                    question.votes.delete(request.user.id)
                # else upvote the question
                else:
                    question.votes.up(request.user.id)
            if request.GET.get("down"):
                # check if user has already downvoted, if yes, remove user's downvote
                if check in user_votes_down.values("user_id"):
                    question.votes.delete(request.user.id)
                # else downvote the question
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
            # return redirect("home:question")
    else:
        # if user is not logged in
        return redirect("users:login")


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
