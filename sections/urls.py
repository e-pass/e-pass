from rest_framework import routers

from sections.views import SectionViewSet

router = routers.DefaultRouter()
router.register(prefix='section', viewset=SectionViewSet, basename='section_api')

urlpatterns = router.urls
