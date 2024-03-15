from typing import Any

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from user_verification.models import ConfirmationCodeModel
from user_verification.serializer import (ConfirmationCodeSerializer,
                                          VerifyCodeSerializer)
from ePass.schema_data import API_METADATA
from users.serializer import UserModelSerializer


# TODO: return SMS confirmation
class SendConfirmationCodeView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmationCodeSerializer

    @swagger_auto_schema(**API_METADATA["SendConfirmationCodeView_post"])
    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.save(validated_data=serializer.validated_data)
            return Response(data={'code': code}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class VerifyConfirmationCode(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer

    @swagger_auto_schema(**API_METADATA["VerifyConfirmationCode_create"])
    def create(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            code_model = ConfirmationCodeModel.get_confirmation_code(code=code)
            code_model.mark_code_as_used()
            access_token = self.get_access_token(user=code_model.user)
            user_data = UserModelSerializer(code_model.user).data
            return Response(data={'access_token': access_token, 'user': user_data},
                            status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_access_token(user: AuthUser) -> str:
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
