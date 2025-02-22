from rest_framework import viewsets
from apps.bot.models.feedback import Feedback
from apps.bot.serializers.feedbacks import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
