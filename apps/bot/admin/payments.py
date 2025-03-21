from django.contrib import admin
from apps.bot.models.payments import Payment
from unfold.admin import ModelAdmin


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    pass
