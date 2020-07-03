import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from autoslug import AutoSlugField


class User(AbstractUser):
    bio = models.TextField(default="")
    display_img = models.ImageField(blank=True, upload_to="users")
    slug = AutoSlugField(populate_from="first_name", unique=True)
    location = models.CharField(max_length=100, blank=True)

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


YEAR_CHOICES = []
for year in range(1980, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((year, year))


class WorkPlace(models.Model):
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True,)
    end_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True,)
    is_currently_working = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name


class Education(models.Model):
    school_name = models.CharField(max_length=100)
    start_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True,)
    end_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True,)
    is_currently_studying = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.school_name
