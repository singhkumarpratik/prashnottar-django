from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from qnA.models import Question, Answer, FollowQuestion


class Notification(models.Model):
    msg = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_from_people"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_to_people"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="notif_question"
    )
    # question_slug = models.SlugField()


@receiver(post_save, sender=Answer)
def notification(sender, **kwargs):
    from_user = kwargs.get("instance").user
    to_user = kwargs.get("instance").question.user
    question = kwargs.get("instance").question
    if from_user != to_user:
        """Not sending notification in scenarios such as user answering his/her own question"""
        Notification.objects.create(
            from_user=from_user,
            to_user=to_user,
            msg=f"{from_user.first_name} {from_user.last_name} answered your question: {question}",
            question=question,
        )
    question_followers = FollowQuestion.objects.filter(question=question)
    for follower in question_followers:
        if from_user != follower.user:
            """
            This ensures that if a user follows a question and then answers that question then he/she
            wouldn't get notification
            """
            Notification.objects.create(
                from_user=from_user,
                to_user=follower.user,
                msg=f"{from_user.first_name} {from_user.last_name} answered a question you were following: {question}",
                question=question,
            )
