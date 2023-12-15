from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


class ConfirmationCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region=settings.PHONE_NUMBER_REGION, required=True)


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6, required=True)
