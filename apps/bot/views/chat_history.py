from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.bot.models import AIChatHistory, TelegramUser, Payment

from apps.bot.serializers.chat_history import AIChatHistorySerializer


class AIChatHistoryViewSet(viewsets.ModelViewSet):
    queryset = AIChatHistory.objects.all()
    serializer_class = AIChatHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get("user")
        return (
            AIChatHistory.objects.filter(user__telegram_id=user_id)
            if user_id
            else AIChatHistory.objects.none()
        )

    def create(self, request, *args, **kwargs):
        telegram_id = request.data.get("telegram_id")

        try:
            user = TelegramUser.objects.get(telegram_id=telegram_id)
        except TelegramUser.DoesNotExist:
            return Response(
                {"error": "User with this telegram_id not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            payment = Payment.objects.create(
                user=user,
                amount=request.data.get("amount"),
                currency=request.data.get("currency"),
                status=request.data.get("status"),
            )
            return Response(
                {"message": "Payment created", "id": payment.id},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
