from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.utils import send_otp_email
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
import pyotp

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "user_type"]
        extra_kwargs = {"id": {"read_only": True}}


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        user = authenticate(email=data["email"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
            },
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        user = self.user
        otp = pyotp.TOTP(user.otp_secret, interval=60).now()

        send_otp_email(user, otp)

        return {"message": "OTP sent to email."}


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)


    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        totp = pyotp.TOTP(user.otp_secret, interval=60)
        if not totp.verify(data["otp"]):
            raise serializers.ValidationError("Invalid OTP.")

        user. set_password(data["new_password"])
        user.save()
        return {"message": "Password reset successful."}
