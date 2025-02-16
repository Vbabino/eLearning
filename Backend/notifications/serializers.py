from rest_framework import serializers
from notifications.models import StatusUpdate

class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUpdate
        fields = "__all__"