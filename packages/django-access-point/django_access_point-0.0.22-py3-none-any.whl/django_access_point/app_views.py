from django_access_point.models.custom_field import CUSTOM_FIELD_STATUS
from django_access_point.models.user import USER_TYPE_CHOICES, USER_STATUS_CHOICES
from django_access_point.views.custom_field import CustomFieldViewSet
from django_access_point.views.crud import CrudViewSet

from django_access_point.utils_response import (
    success_response,
    validation_error_response,
)

from .models import User, UserCustomField, UserCustomFieldValue
from .serializers import UserSerializer, UserCustomFieldSerializer


class PlatformUser(CrudViewSet):
    queryset = User.objects.filter(user_type=USER_TYPE_CHOICES[0][0]).exclude(
        status=USER_STATUS_CHOICES[0][0]
    )
    list_fields = {"id": "ID", "name": "Name", "email": "Email Address"}
    serializer_class = UserSerializer
    custom_field_model = UserCustomField
    custom_field_value_model = UserCustomFieldValue

    @action(detail=False, methods=['post'], url_path='invite')
    def invite_user(self, request, *args, **kwargs):
        """
        Invite a user by email.
        """
        email = request.data.get('email')
        if not email:
            validation_error_response({"email": ["This field is required."]})

        self.send_invite_user_email(email)

    @action(detail=False, methods=['post'], url_path='complete-profile-setup')
    def complete_profile_setup(self, request, *args, **kwargs):
        """
        Complete Profile Setup.
        """
        password = request.data.get('password')

        pass

    def after_save(self, request, instance):
        """
        Handle after save.
        """
        email = instance.email

        self.send_invite_user_email(email)

    def send_invite_user_email(self, email):
        """
        Send invitation email to the user.
        """
        pass


class PlatformUserCustomField(CustomFieldViewSet):
    queryset = UserCustomField.objects.filter(status=CUSTOM_FIELD_STATUS[1][0])
    serializer_class = UserCustomFieldSerializer
