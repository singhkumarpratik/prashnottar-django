from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from qnA.models import Question, Answer, FollowQuestion


class Notification(models.Model):
    msg = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    is_answer = models.BooleanField(default=False)
    is_followed_question = models.BooleanField(default=False)
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_from_people",
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_to_people"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="notif_question"
    )
    created_date = models.DateTimeField(auto_now=True)
    # question_slug = models.SlugField()


@receiver(post_save, sender=Answer)
def notification(sender, **kwargs):
    if kwargs["created"]:
        """
        When a user upvotes/downvotes an answer, the answer model is modified as answer's vote_score is updated. This if condition ensures that notifications are only sent when a new answer is created and not everytime when someone upvotes/downvotes the ans
        """
        from_user = kwargs.get("instance").user
        to_user = kwargs.get("instance").question.user
        question = kwargs.get("instance").question
        is_anonymous = kwargs.get("instance").is_anonymous
        if is_anonymous:
            msg = f"An Anonymous user answered your question: {question}"
        else:
            msg = f"{from_user.first_name} {from_user.last_name} answered your question: {question}"
        if from_user != to_user:
            """Not sending notification in scenarios such as user answering his/her own question"""
            Notification.objects.create(
                from_user=from_user,
                to_user=to_user,
                msg=msg,
                question=question,
                is_anonymous=is_anonymous,
                is_answer=True,
            )
        question_followers = FollowQuestion.objects.filter(question=question)
        if is_anonymous:
            # message to the followers of a question
            msg = (
                f"An Anonymous user answered a question you were following: {question}"
            )
        else:
            msg = f"{from_user.first_name} {from_user.last_name} answered a question you were following: {question}"
        for follower in question_followers:
            if from_user != follower.user:
                """
                This ensures that if a user follows a question and then answers that question then he/she
                wouldn't get notification
                """
                Notification.objects.create(
                    from_user=from_user,
                    to_user=follower.user,
                    msg=msg,
                    question=question,
                    is_followed_question=True,
                )
