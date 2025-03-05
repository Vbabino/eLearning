from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.utils import send_otp_email
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import pyotp
from PIL import Image
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "user_type"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": {"read_only": True},
            "user_type": {"read_only": True},
        }

    def validate(self, data):

        errors = {}
        if "email" in self.initial_data:
            errors["email"] = "Email cannot be modified."
        if "user_type" in self.initial_data:
            errors["user_type"] = "User type cannot be modified."

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)


class UserProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["photo"]

    def validate_photo(self, value):
        """Custom validation to enforce file type and size restrictions."""

        allowed_extensions = ["jpg", "jpeg", "png"]
        file_extension = value.name.split(".")[-1].lower()

        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only JPG, JPEG, and PNG files are allowed."
            )

        # Check file size
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Profile photo size exceeds 5MB.")

        # Manually check if the file is a valid image
        try:
            img = Image.open(value)
            img.verify()  # This will raise an error if it's not an image
        except (IOError, ValidationError):
            raise serializers.ValidationError("Upload a valid image file.")

        return value


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate_first_name(self, value):
        if len(value) >= 255:
            raise serializers.ValidationError(
                "First name must be at most 255 characters."
            )
        return value

    def validate_last_name(self, value):
        if len(value) >= 255:
            raise serializers.ValidationError(
                "Last name must be at most 255 characters."
            )
        return value


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
                "is_approved": user.is_approved,
                "user_type": user.user_type,
            },
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        """Ensure the provided refresh token is valid and not blacklisted."""
        try:
            token = RefreshToken(value)
            token.check_blacklist()
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token.")

        return value


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

        user.set_password(data["new_password"])
        user.save()
        return {"message": "Password reset successful."}
