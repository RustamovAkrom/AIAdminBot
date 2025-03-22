from rest_framework import serializers
from apps.bot.models.payments import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "currency", "status"]
