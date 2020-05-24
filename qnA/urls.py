from django.urls import path
from . import views

app_name = "qnA"
urlpatterns = [
    path("", views.QnaListView.as_view(), name="home"),
    path("<slug:slug>/", views.QuestionDetailView.as_view(), name="question_detail"),
]
