from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.bot.models.feedback import Feedback
from apps.bot.models.users import TelegramUser
from apps.bot.serializers.feedbacks import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        telegram_id = request.data.get("telegram_id")

        try:
            user = TelegramUser.objects.get(telegram_id=telegram_id)
        except TelegramUser.DoesNotExist:
            return Response(
                {"error": "User with this telegram_id not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        feedback_data = {"user": user.id, "message": request.data.get("message")}

        serializer = self.get_serializer(data=feedback_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
