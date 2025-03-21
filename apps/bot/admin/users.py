from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.bot.models.users import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    pass
