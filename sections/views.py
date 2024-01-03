from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sections.models import GroupModel, SectionModel
from sections.serializer import GroupSerializer, SectionSerializer, ShortSectionSerializer
from users.permissions import IsTrainer, IsSectionOwner


class SectionViewSet(ModelViewSet):
    queryset = SectionModel.objects.all()
    serializer_class = SectionSerializer

    def get_permissions(self) -> list:
        method = self.request.method
        if method == 'POST':
            self.permission_classes = (IsTrainer,)
        elif method in ('PUT', 'PATCH', 'DELETE'):
            self.permission_classes = (IsSectionOwner,)

        return super(SectionViewSet, self).get_permissions()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        self.serializer_class = ShortSectionSerializer
        return super().list(request, *args, **kwargs)


class GroupViewSet(ModelViewSet):
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer
