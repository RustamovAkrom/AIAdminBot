from django.utils.translation import gettext_lazy as _
from django.db import models
from apps.shared.models.base import AbstractBaseModel


class Payment(AbstractBaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        "bot.TelegramUser", models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(
        max_length=7, choices=StatusChoices.choices, default=StatusChoices.PENDING.value
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        db_table = "payments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.amount} {self.currency} - {self.status}"
