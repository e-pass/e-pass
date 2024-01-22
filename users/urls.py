from django.urls import path
from rest_framework import routers

from users.views import UserViewSet, UserSearchView

router = routers.DefaultRouter()
router.register(prefix='user', viewset=UserViewSet, basename='user_api')

urlpatterns = [
    path('search/<str:query>/', UserSearchView.as_view(), name='user_search')
]

urlpatterns += router.urls
