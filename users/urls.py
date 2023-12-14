from rest_framework import routers

from users.views import UserViewSet


router = routers.DefaultRouter()
router.register(prefix='user', viewset=UserViewSet, basename='user_api')

urlpatterns = router.urls
