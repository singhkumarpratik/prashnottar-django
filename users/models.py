from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from autoslug import AutoSlugField


class User(AbstractUser):
    bio = models.TextField(default="")
    display_img = models.ImageField(blank=True, upload_to="users")
    slug = AutoSlugField(populate_from="first_name", unique=True)

    def save(self, *args, **kwargs):
        full_name = self.first_name + "-" + self.last_name
        self.slug = slugify(full_name)
        super(User, self).save(*args, **kwargs)
