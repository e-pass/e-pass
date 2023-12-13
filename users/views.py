from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import UserModel
from users.serializer import UserModelCreateSerializer


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelCreateSerializer

    def get_permissions(self) -> list:
        method = self.request.method
        if method == 'POST':
            self.permission_classes = (AllowAny,)
        elif method in ('PUT', 'PATCH', 'DELETE'):
            self.permission_classes = (IsAdminUser,)
        else:
            self.permission_classes = (IsAuthenticated,)

        return super(UserViewSet, self).get_permissions()
