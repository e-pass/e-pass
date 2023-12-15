from rest_framework import routers

from sections.views import SectionViewSet

router = routers.DefaultRouter()
router.register(prefix='sections', viewset=SectionViewSet, basename='section_api')

urlpatterns = router.urls
