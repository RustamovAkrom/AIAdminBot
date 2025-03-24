from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.bot.models.users import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = ("id", "telegram_id", "username", "is_superuser", "is_active")
    fields = ("telegram_id", "username", "full_name", "is_superuser", "is_active")
