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
    path("<int:question_id>/vote", views.vote, name="question-vote"),
    path("question/<slug:slug>/<int:question_id>/vote/", views.vote, name="vote"),
    path("ask-question/", views.AskQuestionView.as_view(), name="ask-question"),
    path("answer/<slug:slug>", views.AnswerView.as_view(), name="answer"),
]
