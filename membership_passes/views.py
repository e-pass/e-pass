from django.db.models import Prefetch
from rest_framework import status
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from membership_passes.models import PassModel
from membership_passes.serializer import PassSerializer, CreatePassSerializer
from membership_passes.validation import (_check_object_entry_in_db_by_id,
                                          _check_object_for_expiration_date, _check_expiration_date)
from sections.models import LessonModel
from users.models import UserModel
from sections.models import SectionModel


class PassListCreateView(generics.ListCreateAPIView):

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return PassSerializer
        return CreatePassSerializer

    def get_queryset(self):
        method = self.request.method
        if method == 'GET':
            return PassModel.objects.filter(section=self.kwargs['section_id']).prefetch_related(
                Prefetch('lessons', queryset=LessonModel.objects.all().only('id', 'lesson_datetime')),
                Prefetch('student', queryset=UserModel.students.all().only(
                    'id', 'first_name', 'last_name', 'phone_number')
                         )
            )
        return PassModel.objects.filter(section=self.kwargs['section_id'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        for item in queryset:
            _check_object_for_expiration_date(item)
            item.refresh_from_db()
        return super(PassListCreateView, self).list(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        section_id = kwargs['section_id']
        if not _check_object_entry_in_db_by_id(model=SectionModel, object_id=section_id):
            return JsonResponse(
                data={'message': f'Секции с id {section_id} не существует. Проверьте параметры запроса'},
                status=status.HTTP_404_NOT_FOUND)
        return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer: ModelSerializer):
        section_id = self.kwargs['section_id']
        section = SectionModel.objects.get(id=section_id)
        serializer.validated_data['section'] = section
        serializer.save()


class PassRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        if self.request.method == 'GET':
            return PassModel.objects.all().prefetch_related(
                Prefetch('lessons', queryset=LessonModel.objects.all().only('id')),
                Prefetch('student', queryset=UserModel.students.all().only(
                    'id', 'first_name', 'last_name', 'phone_number')
                         )
            )
        return PassModel.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return PassSerializer
        return CreatePassSerializer

    def get_object(self):
        obj = super(PassRetrieveUpdateDeleteView, self).get_object()
        obj = _check_object_for_expiration_date(obj)
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if not instance.is_active:
            message = 'Обновление невозможно. Абонемент заблокирован'
            if not _check_expiration_date(instance.valid_until):
                message = 'Обновление невозможно. Срок действия абонемента закончился'
            return JsonResponse(data={'message': message}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
