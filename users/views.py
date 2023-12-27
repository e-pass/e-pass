from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import UserModel, TrainerModel, StudentModel
from users.serializer import UserModelSerializer, TrainerModelSerializer, StudentModelSerializer
from users.permissions import IsOwnerOrStaff, IsSectionOwnerOrGroupTrainerOrAccountOwnerOrStaff


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

    def get_permissions(self) -> list:
        method = self.request.method
        if method == 'POST':
            self.permission_classes = (AllowAny,)
        elif method in ('GET', 'PUT', 'PATCH'):
            self.permission_classes = (IsOwnerOrStaff,)
        elif method == 'DELETE':
            self.permission_classes = (IsAdminUser,)

        return super(UserViewSet, self).get_permissions()


class TrainerViewSet(UserViewSet):
    queryset = TrainerModel.objects.all()
    serializer_class = TrainerModelSerializer

    def get_permissions(self) -> list:
        return super().get_permissions()


class StudentViewSet(UserViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentModelSerializer

    def get_permissions(self) -> list:
        method = self.request.method
        if method == 'POST':
            self.permission_classes = (AllowAny,)
        elif method in ('GET', 'PUT', 'PATCH'):
            self.permission_classes = (IsSectionOwnerOrGroupTrainerOrAccountOwnerOrStaff,)
        elif method == 'DELETE':
            self.permission_classes = (IsAdminUser,)

        return super(StudentViewSet, self).get_permissions()
