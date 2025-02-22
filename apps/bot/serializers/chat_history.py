from rest_framework import serializers
from apps.bot.models.chat_history import AIChatHistory


class AIChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIChatHistory
        fields = "__all__"
