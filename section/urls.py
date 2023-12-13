from django.urls import include, path
from rest_framework import routers

from section.views import SectionViewSet

router = routers.SimpleRouter()
router.register(prefix=r'section', viewset=SectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
