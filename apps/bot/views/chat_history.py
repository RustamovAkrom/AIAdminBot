from rest_framework import viewsets
from apps.bot.models.chat_history import AIChatHistory
from apps.bot.serializers.chat_history import AIChatHistorySerializer


class AIChatHistoryViewSet(viewsets.ModelViewSet):
    queryset = AIChatHistory.objects.all()
    serializer_class = AIChatHistorySerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user")
        return AIChatHistory.objects.filter(user__telegram_id=user_id) if user_id else AIChatHistory.objects.none()
