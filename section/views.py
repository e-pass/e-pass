from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from section.models import SectionModel
from section.serializer import SectionSerializer
from users.permissions import IsOwnerOrStaff


class SectionViewSet(ModelViewSet):
    queryset = SectionModel.objects.all().prefetch_related('owner', 'trainers', 'students')
    serializer_class = SectionSerializer

    def get_permissions(self) -> list:
        method = self.request.method
        if method == 'POST':
            self.permission_classes = (IsAuthenticated,)
        elif method in ('PUT', 'PATCH', 'DELETE'):
            self.permission_classes = (IsOwnerOrStaff,)

        return super(SectionViewSet, self).get_permissions()
