from django.conf import settings
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from users.models import UserModel, OTPModel


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPModel
        fields = ('otp_code', 'otp_expiry', 'max_otp_try', 'otp_max_out')


class UserModelSerializer(serializers.ModelSerializer):
    otp = OTPSerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'phone_number', 'password', 'email', 'first_name', 'last_name',
                  'is_trainer', 'is_active', 'is_staff', 'is_superuser', 'otp')


class UserModelCreateSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region=settings.PHONE_NUMBER_REGION)

    class Meta:
        model = UserModel
        fields = ('phone_number', 'password', 'first_name', 'last_name', 'is_trainer', 'is_superuser')

    def create(self, validated_data):
        if validated_data.get("is_superuser"):
            user = UserModel.objects.create_superuser(**validated_data)
        else:
            user = UserModel.objects.create_user(**validated_data)
        if user:
            OTPModel.objects.create(user=user)
        return user

    def validate_phone_number(self, phone_number):
        if self.Meta.model.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона уже существует.")
        return phone_number
