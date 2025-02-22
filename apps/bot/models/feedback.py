from django.utils.translation import gettext_lazy as _
from django.db import models
from apps.shared.models.base import AbstractBaseModel


class Feedback(AbstractBaseModel):
    user = models.ForeignKey("bot.TelegramUser", models.CASCADE, related_name="feedbacks")
    message = models.TextField()

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")
        db_table = "feedbacks"
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback from {self.user.username or self.user.telegram_id}"
