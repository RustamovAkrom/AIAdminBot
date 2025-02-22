from rest_framework import viewsets
from apps.bot.models.payments import Payment
from apps.bot.serializers.payments import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
