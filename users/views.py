from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import FormView, UpdateView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User, Follow
from .mixins import LogoutRequiredMixin


class UserLoginView(LogoutRequiredMixin, FormView):
    form_class = LoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("qnA:home")


class UserRegisterView(LogoutRequiredMixin, FormView):
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
        is_following = Follow.objects.filter(
            from_user=self.request.user.pk, to_user=user.pk
        )
        context["is_following"] = is_following
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
        is_following = Follow.objects.filter(
            from_user=self.request.user.pk, to_user=user.pk
        )
        context["is_following"] = is_following
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
        answers = user.answer_set.filter(pin_answer=True).order_by("-vote_score")
        is_following = Follow.objects.filter(
            from_user=self.request.user.pk, to_user=user.pk
        )
        context["is_following"] = is_following
        context["answers"] = answers
        return context


class ProfileFollowersListView(ListView):
    model = User
    template_name = "users/user_followers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_slug = self.kwargs.get("slug")
        user = User.objects.get(slug=user_slug)
        is_following = Follow.objects.filter(
            from_user=self.request.user.pk, to_user=user.pk
        )
        followers = Follow.objects.filter(to_user=user.pk)
        context["is_following"] = is_following
        context["followers"] = followers
        context["user"] = user
        return context


class ProfileFollowingListView(ListView):
    model = User
    template_name = "users/user_following.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_slug = self.kwargs.get("slug")
        user = User.objects.get(slug=user_slug)
        is_following = Follow.objects.filter(
            from_user=self.request.user.pk, to_user=user.pk
        )
        following = Follow.objects.filter(from_user=user.pk)
        context["is_following"] = is_following
        context["followings"] = following
        context["user"] = user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/edit.html"
    model = User
    form_class = ProfileForm
    login_url = "/users/login/"
    success_url = reverse_lazy("qnA:home")

    def get_object(self, queryset=None):
        return self.request.user


def profile_answer_pin(request, slug, is_pin, answer_pk):
    if request.user.is_authenticated:
        if request.user.slug == slug:
            user = User.objects.get(slug=slug)
            answers = user.answer_set.filter(pk=answer_pk)
            if is_pin == "pin":
                for answer in answers:
                    answer.pin_answer = True
                    answer.save()
            elif is_pin == "unpin":
                for answer in answers:
                    answer.pin_answer = False
                    answer.save()
            else:
                return redirect("qnA:home")
            return redirect(
                reverse("users:profile_answers", kwargs={"slug": user.slug})
            )
        else:
            return redirect("qnA:home")


def follow_unfollow_users(request, slug):
    if request.user.is_authenticated:
        from_user = request.user
        to_user = User.objects.get(slug=slug)
        if from_user != to_user:
            following = Follow.objects.filter(from_user=from_user, to_user=to_user)
            is_following = False
            if following:
                is_following = True
            if is_following:
                unfollow = Follow.objects.filter(
                    from_user=from_user, to_user=to_user
                ).first()
                unfollow.delete()
                is_following = False
            else:
                follow, created = Follow.objects.get_or_create(
                    from_user=request.user, to_user=to_user
                )
                is_following = True
            return JsonResponse({"is_following": is_following, "is_user_follow": True})
    return redirect("users:login")


def logout_request(request):
    logout(request)
    return redirect("qnA:home")
