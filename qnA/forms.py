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
