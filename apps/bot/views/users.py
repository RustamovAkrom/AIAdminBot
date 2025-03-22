from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.bot.models.users import TelegramUser
from apps.bot.serializers.users import TelegramUserSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["username", "telegram_id"]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def block(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"message": f"Пользователь {user.telegram_id} заблокирован"})

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def unblock(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": f"Пользователь {user.telegram_id} разблокирован"})
