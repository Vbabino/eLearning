from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from accounts.models import USER_TYPES


class CustomRegisterSerializer(RegisterSerializer):
    user_type = serializers.ChoiceField(choices=USER_TYPES, required=True)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.user_type = self.validated_data["user_type"]
        user.save()
        return user
