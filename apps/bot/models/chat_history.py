from django.utils.translation import gettext_lazy as _
from django.db import models
from apps.shared.models.base import AbstractBaseModel


class AIChatHistory(AbstractBaseModel):
    user = models.ForeignKey("bot.TelegramUser", models.CASCADE, related_name="ai_chat_history")
    message = models.TextField()
    response = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = _("AI Chat History")
        verbose_name_plural = _("AI Chat Histories")
        db_table = "ai_chat_histories"
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat with {self.user.username or self.user.telegram_id}"
