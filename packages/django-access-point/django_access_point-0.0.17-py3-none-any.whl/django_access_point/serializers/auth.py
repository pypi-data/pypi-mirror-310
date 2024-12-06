from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate the user
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(_("Invalid credentials"))

        # Check tenant status
        if hasattr(user, 'tenant') and user.tenant:
            tenant = user.tenant
            if tenant.status != 'active':  # Assuming 'active' is the tenant status
                raise serializers.ValidationError(_("Tenant account is not active"))

        attrs['user'] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

