from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(default="")
    display_img = models.ImageField(blank=True, upload_to="users")
