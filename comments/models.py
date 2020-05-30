from django.db import models
from django_comments_xtd.models import XtdComment
from vote.models import VoteModel
from users.models import User


class MyComment(VoteModel, XtdComment):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=18)
    pass
