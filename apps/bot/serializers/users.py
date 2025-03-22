from rest_framework import serializers
from apps.bot.models.users import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = [
            "id",
            "telegram_id",
            "full_name",
            "username",
            "is_superuser",
            "is_active",
        ]
