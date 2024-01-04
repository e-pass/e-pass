from django.urls import path
from rest_framework import routers

from sections.views import (GroupListCreateAPIView,
                            GroupRetrieveUpdateDestroyAPIView, SectionViewSet)

router = routers.DefaultRouter()
router.register(prefix='section', viewset=SectionViewSet, basename='section_api')

urlpatterns = [
    path('section/<int:section_id>/group/', GroupListCreateAPIView.as_view(), name='group_list_create'),
    path(
        'section/<int:section_id>/group/<int:group_id>/',
        GroupRetrieveUpdateDestroyAPIView.as_view(),
        name='group_RUD')
] + router.urls
