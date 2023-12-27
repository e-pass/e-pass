from rest_framework import routers

from sections.views import SectionViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(prefix='section', viewset=SectionViewSet, basename='section_api')
router.register(prefix='group', viewset=GroupViewSet, basename='group_api')

urlpatterns = router.urls
