from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView, UpdateView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User


class UserLoginView(FormView):
    form_class = LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("qnA:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UserRegisterView(FormView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("qnA:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class ProfileAnswerListView(ListView):
    model = User
    template_name = "users/user_answers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_slug = self.kwargs.get("slug")
        user = User.objects.get(slug=user_slug)
        answers = user.answer_set.all()
        print(answers)
        context["answers"] = answers
        context["user"] = user
        return context


class ProfileQuestionListView(ListView):
    model = User
    template_name = "users/user_questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_slug = self.kwargs.get("slug")
        user = User.objects.get(slug=user_slug)
        questions = user.question_set.all()
        context["questions"] = questions
        context["user"] = user
        return context


class ProfileDetailView(DetailView):
    """This view shows answers pinned by the user"""

    queryset = User.objects.all()
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.get_object().pk)
        # answers = user.answer_set.all()
        answers = user.answer_set.filter(pin_answer=True).order_by("-vote_score")
        context["answers"] = answers
        return context


class ProfileUpdateView(UpdateView):
    template_name = "users/edit.html"
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy("qnA:home")

    def get_object(self, queryset=None):
        return self.request.user


def logout_request(request):
    logout(request)
    return redirect("qnA:home")
