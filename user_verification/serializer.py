import random

from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from user_verification.models import ConfirmationCodeModel
from users.models import UserModel


class ConfirmationCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region=settings.PHONE_NUMBER_REGION, required=True)

    def create(self, validated_data: dict) -> dict:
        phone_number = validated_data.get('phone_number')

        user = UserModel.objects.get(phone_number=phone_number)
        code = self.__generate_confirmation_code()
        ConfirmationCodeModel.objects.create(user=user, code=f'{code}')

        # Здесь должна быть логика отправки смс с кодом на указанный номер

        return {'user': user, 'code': code}

    @staticmethod
    def __generate_confirmation_code() -> int:
        return random.randint(111111, 999999)


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6, required=True)

    @staticmethod
    def validate_code(code: str) -> str:
        code_model = ConfirmationCodeModel.get_confirmation_code(code=code)

        if not code_model or code_model.is_expired() or not code_model.is_valid:
            raise serializers.ValidationError('Invalid or expired code')

        return code
