import random

from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from user_verification.services.sms_service import send_sms_with_code
from user_verification.models import ConfirmationCodeModel
from users.models import UserModel


class ConfirmationCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region=settings.PHONE_NUMBER_REGION, required=True)

    def create(self, validated_data: dict) -> dict:
        phone_number = validated_data.get('phone_number')
        code = self.__generate_confirmation_code()
        user = UserModel.objects.get(phone_number=phone_number)
        ConfirmationCodeModel.objects.create(user=user, code=f'{code}')
        sms_result = send_sms_with_code(phone_number=phone_number, code=code)
        return sms_result

    @staticmethod
    def validate_phone_number(phone_number: str) -> str:
        if not UserModel.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Пользователя с введенным номером телефона не существует')
        return phone_number

    @staticmethod
    def __generate_confirmation_code() -> int:
        return random.randint(1111, 9999)


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=4, max_length=4, required=True)

    @staticmethod
    def validate_code(code: str) -> str:
        code_model = ConfirmationCodeModel.get_confirmation_code(code=code)

        if not code_model or code_model.is_expired() or not code_model.is_valid:
            raise serializers.ValidationError('Неправильный код или истек срок действия')

        return code
