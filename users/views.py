from rest_framework.viewsets import ModelViewSet

from .models import UserModel
from .serializer import UserModelSerializer, UserModelCreateSerializer


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all().select_related('otp')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserModelSerializer
        return UserModelCreateSerializer
