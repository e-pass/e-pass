from typing import Any

from rest_framework import generics, status
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sections.utils.exception_handlers import UniqueUserHandler
from users.managers import UserQuerySet
from users.models import UserModel
from users.permissions import IsOwnerOrStaff, IsTrainer
from users.serializer import ShortUserSerializer, UserModelSerializer


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    search_fields = ('^phone_number',)
    filterset_fields = ('is_trainer',)

    def get_permissions(self) -> list:
        method = self.request.method
        if method == 'POST':
            self.permission_classes = (AllowAny,)
        elif method in ('GET', 'PUT', 'PATCH'):
            self.permission_classes = (IsOwnerOrStaff,)
        elif method == 'DELETE':
            self.permission_classes = (IsAdminUser,)

        return super(UserViewSet, self).get_permissions()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        phone_number = request.data.get('phone_number')
        if UserModel.objects.filter(phone_number=phone_number).exists():
            raise UniqueUserHandler()
        return super().create(request, *args, **kwargs)


class UserSearchView(generics.ListAPIView):
    permission_classes = [IsTrainer]
    serializer_class = ShortUserSerializer

    def get_queryset(self) -> UserQuerySet:
        query = self.kwargs["query"]
        if query is not None:
            queryset = UserModel.objects.search(query=query)
            return queryset
        return UserModel.objects.none()
