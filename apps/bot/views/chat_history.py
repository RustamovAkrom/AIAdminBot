from rest_framework import viewsets
from apps.bot.models.chat_history import AIChatHistory
from apps.bot.serializers.chat_history import AIChatHistorySerializer


class AIChatHistoryViewSet(viewsets.ModelViewSet):
    queryset = AIChatHistory.objects.all()
    serializer_class = AIChatHistorySerializer
