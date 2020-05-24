from django.urls import path
from . import views

urlpatterns = [
    path("", views.QnaListView.as_view()),
]
