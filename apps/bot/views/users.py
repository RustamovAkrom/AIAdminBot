from rest_framework import viewsets
from apps.bot.models.users import TelegramUser
from apps.bot.serializers.users import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
