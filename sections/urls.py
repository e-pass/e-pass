from django.urls import path
from rest_framework import routers

from sections.views import (GroupListCreateAPIView,
                            GroupRetrieveUpdateDestroyAPIView, SectionViewSet, LessonRetrieveUpdateDestroyAPIView,
                            LessonListCreateAPIView)

router = routers.DefaultRouter()
router.register(prefix='section', viewset=SectionViewSet, basename='section_api')

urlpatterns = [
    path('section/<int:section_id>/group/', GroupListCreateAPIView.as_view(), name='group_list_create'),
    path(
      'section/<int:section_id>/group/<int:group_id>/',
      GroupRetrieveUpdateDestroyAPIView.as_view(),
      name='group_RUD'
    ),
    path('section/<int:section_id>/lesson/', LessonListCreateAPIView.as_view(), name='lesson_list_create'),
    path(
        'section/<int:section_id>/lesson/<int:lesson_id>/',
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name='lesson_RUD'
    )
] + router.urls
