from typing import Any

from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import OTPModel, UserModel


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPModel
        fields = ('otp_code', 'otp_expiry', 'max_otp_try', 'otp_max_out')


class UserModelSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region=settings.PHONE_NUMBER_REGION, required=True)
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    is_phone_number_verified = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = UserModel
        fields = ('phone_number', 'first_name', 'last_name', 'is_trainer',
                  'is_phone_number_verified', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        if user:
            OTPModel.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        if validated_data.get('phone_number'):
            instance.is_phone_number_verified = False
        instance = super(UserModelSerializer, self).update(instance, validated_data)
        return instance

    def validate_phone_number(self, phone_number):
        if self.Meta.model.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона уже существует.")
        return phone_number
