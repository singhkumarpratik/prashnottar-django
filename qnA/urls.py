from django.urls import path
from . import views

app_name = "qnA"
urlpatterns = [
    path("", views.QnaListView.as_view(), name="home"),
    path(
        "question/<slug:slug>/",
        views.QuestionDetailView.as_view(),
        name="question_detail",
    ),
    # passing slugs for SEO purpose
    path(
        "question/<slug:slug>/answer/<slug:user_slug>/<int:question_pk>/<int:user_pk>",
        views.AnswerDetailView.as_view(),
        name="answer_detail",
    ),
    path("ask-question/", views.AskQuestionView.as_view(), name="ask-question"),
    path("answer/<slug:slug>", views.AnswerView.as_view(), name="answer"),
    path("answer/edit/<slug:slug>", views.AnswerUpdateView.as_view(), name="edit"),
    path("answer/delete/<slug:slug>", views.AnswerDeleteView.as_view(), name="delete"),
    path(
        "question/follow/<slug:question_slug>",
        views.follow_question,
        name="follow-question",
    ),
    path("<int:question_id>/vote", views.vote, name="question-vote"),
    path("question/<slug:slug>/<int:question_id>/vote/", views.vote, name="vote"),
    path("search/", views.QnaListView.as_view(), name="search"),
]
