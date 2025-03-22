from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from apps.bot.models.payments import Payment
from apps.bot.models.users import TelegramUser
from apps.bot.serializers.payments import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get("user")
        return Payment.objects.filter(user__telegram_id=user_id)

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        telegram_id = request.data.get("telegram_id")
        amount = request.data.get("amount")
        currency = request.data.get("currency")
        status_payment = request.data.get("status", "pending")

        try:
            user = TelegramUser.objects.get(telegram_id=telegram_id)
        except TelegramUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            currency=currency,
            status=status_payment,
        )

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
