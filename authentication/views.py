import random
from typing import Any, Optional

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import ConfirmationCodeModel
from authentication.serializer import (ConfirmationCodeSerializer,
                                       VerifyCodeSerializer)
from users.models import UserModel


class SendConfirmationCodeView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        serializer = ConfirmationCodeSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = request.data.get('phone_number')

            if UserModel.objects.filter(phone_number=phone_number).exists():
                user = UserModel.objects.get(phone_number=phone_number)
                code = self.generate_confirmation_code()
                ConfirmationCodeModel.objects.create(user=user, code=f'{code}')

                # Здесь должна быть логика отправки смс с кодом на указанный номер

                return Response(data={'code': code}, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def generate_confirmation_code() -> int:
        return random.randint(111111, 999999)


class VerifyConfirmationCode(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = request.data.get('code')
            code_model_obj = self.get_confirmation_code_model(code=code)

            if all((code_model_obj, not code_model_obj.is_expired(), code_model_obj.is_valid)):
                code_model_obj.is_valid = False
                code_model_obj.save()

                access_token = self.get_access_token(code_model_obj.user)
                return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_confirmation_code_model(code: str) -> Optional[ConfirmationCodeModel]:
        try:
            return ConfirmationCodeModel.objects.get(code=code)
        except ConfirmationCodeModel.DoesNotExist:
            return None

    @staticmethod
    def get_access_token(user: AuthUser) -> str:
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
