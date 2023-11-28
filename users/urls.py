from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet


router = routers.SimpleRouter()
router.register(prefix=r'user', viewset=UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
