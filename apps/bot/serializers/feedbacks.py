from rest_framework import serializers
from apps.bot.models.feedback import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "user", "message", "created_at", "updated_at"]
