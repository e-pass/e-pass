from rest_framework.routers import SimpleRouter

from membership_passes.views import PassModelViewSet

router = SimpleRouter()
router.register(prefix='pass', viewset=PassModelViewSet, basename='pass_api')

urlpatterns = router.urls
