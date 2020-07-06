from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django import forms
from .models import User, WorkPlace, Education


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Enter Email",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Email"}
        ),
    )
    password = forms.CharField(
        label="Enter password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password"}
        ),
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password Incorrect"))
        except:
            self.add_error("email", forms.ValidationError("User Doesn't Exist"))

        return email

    def save(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Last Name"}
        ),
    )
    email = forms.EmailField(
        label="Enter email",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Email"}
        ),
    )
    password = forms.CharField(
        label="Enter password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password"}
        ),
        validators=[validate_password],
    )
    password1 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
        validators=[validate_password],
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("User Already exists")
        except User.DoesNotExist:
            return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password = self.cleaned_data.get("password")
        if password1 != password:
            raise forms.ValidationError(
                "Password and Confirmation Password does not match."
            )
        else:
            return password1

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        createdUser = User.objects.create_user(email, email, password)
        createdUser.first_name = first_name
        createdUser.last_name = last_name
        createdUser.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "bio",
            "location",
            "display_img",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Last Name"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Location"}
            ),
            "bio": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter Bio", "rows": 3,}
            ),
        }


class WorkPlaceForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = (
            "company_name",
            "position",
            "start_year",
            "end_year",
            "is_currently_working",
        )
        widgets = {
            "company_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Company Name"}
            ),
            "position": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Your Position"}
            ),
            "start_year": forms.Select(attrs={"class": "form-control",}),
            "end_year": forms.Select(attrs={"class": "form-control",}),
        }
        labels = {
            "is_currently_working": "Currently Working",
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = (
            "school_name",
            "start_year",
            "end_year",
            "is_currently_studying",
        )
        widgets = {
            "school_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter School Name"}
            ),
            "start_year": forms.Select(attrs={"class": "form-control",}),
            "end_year": forms.Select(attrs={"class": "form-control",}),
        }
        labels = {
            "is_currently_studying": "Currently Studying",
        }
