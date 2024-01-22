from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from users.managers import UserQuerySet
from users.models import UserModel
from users.permissions import IsOwnerOrStaff, IsTrainer
from users.serializer import UserModelSerializer, ShortUserSerializer


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


class UserSearchView(generics.ListAPIView):
    permission_classes = [IsTrainer]
    serializer_class = ShortUserSerializer

    def get_queryset(self) -> UserQuerySet:
        query = self.kwargs["query"]
        if query is not None:
            queryset = UserModel.objects.search(query=query)
            return queryset
        return UserModel.objects.none()
