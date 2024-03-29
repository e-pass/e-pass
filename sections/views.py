from typing import Any

from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sections.models import GroupModel, LessonModel, SectionModel
from sections.serializer import (GroupSerializer, LessonSerializer,
                                 SectionSerializer, ShortGroupSerializer,
                                 ShortSectionSerializer)
from users.permissions import IsSectionOwner, IsTrainer


class SectionViewSet(ModelViewSet):
    queryset = SectionModel.objects.all()
    serializer_class = SectionSerializer
    lookup_url_kwarg = 'section_id'
    search_fields = ('^title',)

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


class GroupListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'section_id'
    search_fields = ('^name',)

    def get_queryset(self) -> QuerySet:
        section_id = self.kwargs.get(self.lookup_url_kwarg)
        return GroupModel.objects.filter(section_id=section_id)

    def perform_create(self, serializer: GroupSerializer) -> None:
        section_id = self.kwargs.get(self.lookup_url_kwarg)
        section = get_object_or_404(SectionModel, id=section_id)
        serializer.save(section=section)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        self.serializer_class = ShortGroupSerializer
        return super().list(request, *args, **kwargs)


class GroupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'group_id'
    section_lookup_url_kwarg = 'section_id'

    def get_object(self) -> Any:
        section_id = self.kwargs.get(self.section_lookup_url_kwarg)
        group_id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(GroupModel, section_id=section_id, id=group_id)


class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    queryset = LessonModel.objects.all()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        section_id = request.query_params.get('section_id')
        if section_id:
            self.queryset = LessonModel.objects.filter(group__section__id=section_id)
        return super().list(request, *args, **kwargs)
