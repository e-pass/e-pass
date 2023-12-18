import random
from typing import Any, Optional

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.tokens import RefreshToken

from user_verification.models import ConfirmationCodeModel
from user_verification.serializer import (ConfirmationCodeSerializer,
                                          VerifyCodeSerializer)
from users.models import UserModel


class SendConfirmationCodeView(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.save()

            return Response(data={'code': data['code']}, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyConfirmationCode(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = request.data.get('code')
            code_model_obj = self.get_confirmation_code_model(code=code)

            if all((code_model_obj, not code_model_obj.is_expired(), code_model_obj.is_valid)):
                code_model_obj.is_valid = False
                code_model_obj.user.is_phone_number_verified = True
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
