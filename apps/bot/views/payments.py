from rest_framework import viewsets
from apps.bot.models.payments import Payment
from apps.bot.serializers.payments import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user")
        return Payment.objects.filter(user__telegram_id=user_id)
