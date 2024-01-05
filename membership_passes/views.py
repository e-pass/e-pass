from django.db.models import Prefetch
from rest_framework import viewsets

from membership_passes.models import PassModel
from membership_passes.serializer import PassSerializer, CreatePassSerializer, UpdatePassSerializer
from sections.models import LessonModel


class PassModelViewSet(viewsets.ModelViewSet):
    queryset = PassModel.objects.all().prefetch_related(
        Prefetch('lessons', queryset=LessonModel.objects.all().only('id'))
    )

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return PassSerializer
        elif method == 'POST':
            return CreatePassSerializer
        elif method in ('PUT', 'PATCH', 'DELETE'):
            return UpdatePassSerializer
