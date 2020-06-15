from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from autoslug import AutoSlugField


class User(AbstractUser):
    bio = models.TextField(default="")
    display_img = models.ImageField(blank=True, upload_to="users")
    slug = AutoSlugField(populate_from="first_name", unique=True)
    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        full_name = self.first_name + "-" + self.last_name
        self.slug = slugify(full_name)
        super(User, self).save(*args, **kwargs)


class Follow(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_people"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="to_people"
    )

    def __str__(self):
        return f"{self.from_user} follows {self.to_user}"
