from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django_access_point.serializers.auth import (
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserOnboardSerializer,
)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Send tokens as response
            return Response(
                {
                    "status": "success",
                    "data": {"refresh": str(refresh), "access": str(access_token)},
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"status": "validation_error", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Fetch the user
        email = serializer.validated_data["email"]
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Generate password reset token
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(user.pk.encode())

        # Send password reset link via email
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}"

        # Prepare the email context
        context = {
            "user": user,
            "reset_url": reset_url,
            "support_email": "support@yourdomain.com",
            "platform_name": "Your Platform Name",
            "logo_url": "https://yourdomain.com/static/logo.png",
            "current_year": 2024,
        }

        # Render the email content (HTML)
        subject = "Reset Your Password"
        message = render_to_string("password_reset_email.html", context)

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,  # Ensure HTML is sent
        )

        return Response(
            {"detail": "Password reset email sent."}, status=status.HTTP_200_OK
        )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            # Decode user ID
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (ValueError, TypeError, get_user_model().DoesNotExist):
            return Response(
                {"detail": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and set new password
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Password successfully reset."}, status=status.HTTP_200_OK
        )


class UserOnboardView(generics.GenericAPIView):
    serializer_class = UserOnboardSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "status": "success",
                    "data": {"user": {"email": user.email, "tenant": user.tenant.name}},
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"status": "validation_error", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
