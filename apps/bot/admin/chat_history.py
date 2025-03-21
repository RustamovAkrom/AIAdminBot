from django.contrib import admin
from apps.bot.models.chat_history import AIChatHistory
from unfold.admin import ModelAdmin


@admin.register(AIChatHistory)
class AIChatHistoryAdmin(ModelAdmin):
    pass
