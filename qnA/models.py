from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from autoslug import AutoSlugField
from vote.models import VoteModel
from users import models as userModels


class Topic(models.Model):

    topic = models.CharField(max_length=255)

    def __str__(self):
        return self.topic


class Question(VoteModel, models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", unique=True)
    user = models.ForeignKey(userModels.User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    topics = models.ManyToManyField(Topic, blank=True)
    rank = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ["-vote_score"]


class Answer(VoteModel, models.Model):
    class Meta:
        ordering = ["-vote_score"]

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans = models.TextField()
    user = models.ForeignKey(userModels.User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    pin_answer = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("qnA:question_detail", kwargs={"slug": self.question.slug,},)

    def __str__(self):
        return f"{self.user.first_name} on {self.created_date}"


class FollowQuestion(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="follow_question",
    )
    user = models.ForeignKey(
        userModels.User, on_delete=models.CASCADE, related_name="follow_question_by"
    )
