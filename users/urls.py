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
    path(
        "profile/<slug:slug>/followers",
        views.ProfileFollowersListView.as_view(),
        name="followers",
    ),
    path(
        "profile/<slug:slug>/following",
        views.ProfileFollowingListView.as_view(),
        name="following",
    ),
    path("edit/", views.ProfileUpdateView.as_view(), name="edit"),
    path(
        "follow_unfollow/<slug:slug>",
        views.follow_unfollow_users,
        name="follow_unfollow",
    ),
    path("logout/", views.logout_request, name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
]
