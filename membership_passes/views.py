from typing import Any
import datetime

from django.db.models import Prefetch
from rest_framework import status
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.response import Response

from membership_passes.models import PassModel
from membership_passes.serializer import PassSerializer, CreatePassSerializer
from sections.models import LessonModel
from users.models import UserModel
from sections.models import SectionModel


def _check_object_entry_in_db_by_id(model: Any, object_id: int) -> bool:
    return model.objects.filter(id=object_id).exists()

def _check_expiration_date(instance: PassModel):
    if instance.valid_until < datetime.date.today():
        instance.is_active = False
        instance.save()
    return instance


class PassListCreateView(generics.ListCreateAPIView):

    def dispatch(self, request, *args, **kwargs):
        section_id = kwargs['section_id']
        if not _check_object_entry_in_db_by_id(model=SectionModel, object_id=section_id):
            return JsonResponse(
                data={'message': f'Секции с id {section_id} не существует. Проверьте параметры запроса'},
                status=status.HTTP_404_NOT_FOUND)
        return super().dispatch(request, *args, **kwargs)

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

    def perform_create(self, serializer):
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = _check_expiration_date(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

