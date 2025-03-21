from django.contrib import admin
from apps.bot.models.feedback import Feedback
from unfold.admin import ModelAdmin


@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    pass
