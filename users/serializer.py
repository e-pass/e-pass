from typing import Any

from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import StudentModel, TrainerModel, UserModel


class UserModelSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region=settings.PHONE_NUMBER_REGION, required=True)
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    is_phone_number_verified = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = UserModel
        fields = ('id', 'phone_number', 'first_name', 'last_name',
                  'is_phone_number_verified', 'created_at', 'updated_at')

    def update(self, instance, validated_data: dict) -> Any:
        if validated_data.get('phone_number'):
            instance.is_phone_number_verified = False

        return super(UserModelSerializer, self).update(instance, validated_data)

    def validate_phone_number(self, phone_number: str) -> str:
        if self.Meta.model.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Пользователь с таким номером телефона уже существует.')
        return phone_number


class TrainerModelSerializer(UserModelSerializer):

    class Meta:
        model = TrainerModel
        fields = ('id', 'phone_number', 'first_name', 'last_name',
                  'is_phone_number_verified', 'created_at', 'updated_at',)


class StudentModelSerializer(UserModelSerializer):
    parent_phone = PhoneNumberField(region=settings.PHONE_NUMBER_REGION, required=False)
    parent_name = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = StudentModel
        fields = ('id', 'phone_number', 'first_name', 'last_name',
                  'is_phone_number_verified', 'created_at', 'updated_at',
                  'parent_phone', 'parent_name',)
