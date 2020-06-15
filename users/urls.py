from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("profile/<slug:slug>", views.ProfileDetailView.as_view(), name="profile"),
    path(
        "profile/<slug:slug>/questions",
        views.ProfileQuestionListView.as_view(),
        name="profile_questions",
    ),
    path(
        "profile/<slug:slug>/answers",
        views.ProfileAnswerListView.as_view(),
        name="profile_answers",
    ),
    path(
        "profile/<slug:slug>/answers/<str:is_pin>/<int:answer_pk>",
        views.profile_answer_pin,
        name="is_pin_answer",
    ),
    path("edit/", views.ProfileUpdateView.as_view(), name="edit"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("logout/", views.logout_request, name="logout"),
]
