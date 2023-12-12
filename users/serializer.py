from django.contrib.auth.models import AbstractUser
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    phone_number = PhoneNumberField(required=True)
    is_trainer = serializers.BooleanField(required=True)

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'phone_number', 'is_trainer')

    def validate_phone_number(self, value: PhoneNumberField) -> PhoneNumberField:
        if self.Meta.model.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона уже существует.")
        return value

    def create(self, validated_data: dict) -> AbstractUser:
        user = UserModel.objects.create_user(**validated_data)
        return user
