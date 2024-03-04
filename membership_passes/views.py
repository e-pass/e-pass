from typing import Any

from django.db.models import Prefetch, Count, F, QuerySet
from rest_framework import status
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.serializers import ModelSerializer

from membership_passes.models import PassModel, EntryModel
from membership_passes.serializer import PassSerializer, CreatePassSerializer, EntrySerializer
from membership_passes.validation import get_section_object_from_db, check_expiration_date
from users.models import UserModel
from users.permissions import IsPassStudentOrTrainerOrSectionOwner, IsTrainerOrSectionOwner, IsTrainer



class EntryCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsTrainer)
    queryset = EntryModel.objects.all()
    serializer_class = EntrySerializer


class PassListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsTrainer)

    def get_queryset(self) -> QuerySet:
        method = self.request.method
        if method == 'GET':
            return PassModel.objects.annotate(
                quantity_unused_lessons=F('quantity_lessons_max') - Count('entries')).filter(
                section=self.kwargs['section_id']).prefetch_related(
                Prefetch('entries', queryset=EntryModel.objects.all()),
                Prefetch('student', queryset=UserModel.students.all().only(
                    'id', 'first_name', 'last_name', 'phone_number')
                         )
            )
        return PassModel.objects.filter(section=self.kwargs['section_id'])

    def get_serializer_class(self) -> Any:
        method = self.request.method
        if method == 'GET':
            return PassSerializer
        return CreatePassSerializer

    def dispatch(self, request: Request, *args: Any, **kwargs: Any) -> Any:
        get_section_object_from_db(self.kwargs['section_id'])
        return super(PassListCreateView, self).dispatch(request, *args, **kwargs)

    def perform_create(self, serializer: ModelSerializer) -> None:
        section = get_section_object_from_db(section_id=self.kwargs['section_id'], need_return=True)
        serializer.validated_data['section'] = section
        serializer.save()


class PassRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self) -> QuerySet:
        if self.request.method == 'GET':
            return PassModel.objects.all().annotate(
                quantity_unused_lessons=F('quantity_lessons_max') - Count('entries')
            ).prefetch_related(
                'entries',
                Prefetch('student', queryset=UserModel.students.all().only(
                    'id', 'first_name', 'last_name', 'phone_number')
                         )
            )
        return PassModel.objects.all().prefetch_related(
            Prefetch('student', queryset=UserModel.students.all().only(
                'id', 'first_name', 'last_name', 'phone_number')
                     )
        )

    def get_serializer_class(self) -> Any:
        if self.request.method == 'GET':
            return PassSerializer
        return CreatePassSerializer

    def get_permissions(self) -> list:
        if self.request.method == 'GET':
            self.permission_classes = (IsAuthenticated, IsPassStudentOrTrainerOrSectionOwner,)
        else:
            self.permission_classes = (IsAuthenticated, IsTrainerOrSectionOwner,)
        return super(PassRetrieveUpdateDeleteView, self).get_permissions()

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response | JsonResponse:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if not instance.is_active:
            message = 'Обновление невозможно. Абонемент заблокирован'
            if not check_expiration_date(instance.valid_until):
                message = 'Обновление невозможно. Срок действия абонемента закончился'
            return JsonResponse(data={'message': message}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
