from django.urls import path
from . import views

urlpatterns = [
    path("", views.QnaListView.as_view()),
    path("<slug:slug>/", views.QuestionDetailView.as_view(), name="question_detail"),
]
