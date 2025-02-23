from django.utils.translation import gettext_lazy as _
from django.db import models
from apps.shared.models.base import AbstractBaseModel


class TelegramUser(AbstractBaseModel):
    telegram_id = models.BigIntegerField(unique=True, verbose_name=_("Telegram ID"))
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Username"))
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Full Name"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Superuser"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Telegram User")
        verbose_name_plural = _("Telegram Users")
        db_table = "telegram_users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username or str(self.telegram_id)
