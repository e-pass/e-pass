from rest_framework.viewsets import ModelViewSet

from sections.models import GroupModel, SectionModel
from sections.serializer import GroupSerializer, SectionSerializer
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


class GroupViewSet(ModelViewSet):
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer
