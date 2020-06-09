from django.forms import ModelForm
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            "title",
            "description",
            "is_anonymous",
        ]
        widgets = {
            "description": SummernoteWidget(),
        }


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
