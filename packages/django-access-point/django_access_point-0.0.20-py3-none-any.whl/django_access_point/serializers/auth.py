from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from django_access_point.models.user import USER_TYPE_CHOICES, USER_STATUS_CHOICES
from django_access_point.utils import get_tenant_model

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Authenticate the user
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(_("Invalid credentials"))

        # Check if the user is active
        if not user.is_user_active():
            raise serializers.ValidationError(_("Your account is not active"))

        # Check tenant status
        if hasattr(user, "tenant") and user.tenant:
            tenant = user.tenant
            if tenant.status != "active":  # Assuming 'active' is the tenant status
                raise serializers.ValidationError(_("Tenant account is not active"))

        attrs["user"] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        You can optionally add logic here to validate email existence.
        This avoids disclosing whether the email exists in the system.
        """
        return value


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        # Optionally, add password strength validation
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        return value


class UserOnboardSerializer(serializers.Serializer):
    tenant_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        tenant_name = validated_data.get("tenant_name")
        email = validated_data.get("email")
        password = validated_data.get("password")

        tenant = get_tenant_model().objects.create(name=tenant_name)

        # Create user and associate with tenant
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            tenant=tenant,
            user_type=USER_TYPE_CHOICES[1][0],
            status=USER_STATUS_CHOICES[1][0]
        )

        tenant.owner = user
        tenant.save()

        return user
