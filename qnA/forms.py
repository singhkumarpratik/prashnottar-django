from django import forms
from django.forms import ModelForm
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            "title",
            "is_anonymous",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control input-lg",
                    "placeholder": "What is your question?",
                    "style": "height: 70px;",
                }
            ),
        }
        labels = {"title": "", "is_anonymous": "Ask Anonymously"}


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = [
            "ans",
            "is_anonymous",
        ]
        widgets = {
            "ans": SummernoteWidget(),
        }
        labels = {"ans": "", "is_anonymous": "Answer Anonymously"}
