from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import UserModel
from users.serializer import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self) -> list:
        method = self.request.method
        if method == 'POST':
            self.permission_classes = (AllowAny,)
        elif method in ('PUT', 'PATCH'):
            self.permission_classes = (IsAdminUser,)
        else:
            self.permission_classes = (IsAuthenticated,)

        return super(UserViewSet, self).get_permissions()
