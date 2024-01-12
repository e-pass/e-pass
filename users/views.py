from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from users.models import UserModel
from users.permissions import IsOwnerOrStaff
from users.serializer import UserModelSerializer


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('phone_number',)

    def get_permissions(self) -> list:
        method = self.request.method
        if method == 'POST':
            self.permission_classes = (AllowAny,)
        elif method in ('GET', 'PUT', 'PATCH'):
            self.permission_classes = (IsOwnerOrStaff,)
        elif method == 'DELETE':
            self.permission_classes = (IsAdminUser,)

        return super(UserViewSet, self).get_permissions()
