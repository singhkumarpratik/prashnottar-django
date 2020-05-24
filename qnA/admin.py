from django.contrib import admin
from . import models


@admin.register(models.Question)
class CustomQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer)
class CustomQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Topic)
class CustomQuestionAdmin(admin.ModelAdmin):
    pass
