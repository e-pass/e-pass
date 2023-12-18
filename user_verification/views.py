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

    def create(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.save()

            return Response(data={'code': data['code']}, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyConfirmationCode(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer

    def create(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            code_model = ConfirmationCodeModel.get_confirmation_code(code=code)
            code_model.mark_code_as_used()
            access_token = self.get_access_token(user=code_model.user)

            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_access_token(user: AuthUser) -> str:
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
