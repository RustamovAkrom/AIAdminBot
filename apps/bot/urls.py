from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TelegramUserViewSet,
    AIChatHistoryViewSet,
    PaymentViewSet,
    FeedbackViewSet,
    stripe_webhook
)

router = DefaultRouter()
router.register(r"telegram_users", TelegramUserViewSet)
router.register(r"ai_chat_history", AIChatHistoryViewSet)
router.register(r"payments", PaymentViewSet)
router.register(r"feedback", FeedbackViewSet)

urlpatterns = [
    path("bot/", include(router.urls)),
    path("bot/webhook/", stripe_webhook, name="stripe_webhook"),
]
