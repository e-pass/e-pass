from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet


router = SimpleRouter()
router.register(prefix=r'user', viewset=UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
