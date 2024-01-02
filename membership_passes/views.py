from django.db.models import Count, F
from rest_framework import viewsets

from membership_passes.models import PassModel
from membership_passes.serializer import PassSerializer, CreatePassSerializer, UpdatePassSerializer


class PassModelViewSet(viewsets.ModelViewSet):
    queryset = PassModel.objects.all().annotate(
        unused_lessons=F('quantity_lessons_max') - Count('lessons')
        ).select_related('student', 'section', 'group').select_related('student', 'section', 'group'
                                                                       ).prefetch_related('lessons')

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return PassSerializer
        elif method == 'POST':
            return CreatePassSerializer
        elif method in ('PUT', 'PATCH', 'DELETE'):
            return UpdatePassSerializer





