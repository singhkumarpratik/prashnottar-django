from django.contrib import admin
from . import models


@admin.register(models.Notification)
class CustomQuestionAdmin(admin.ModelAdmin):
    pass
