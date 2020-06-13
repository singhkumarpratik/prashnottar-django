from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("edit/", views.ProfileUpdateView.as_view(), name="edit"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("logout/", views.logout_request, name="logout"),
]
