from rest_framework import routers

from users.views import UserViewSet, TrainerViewSet, StudentViewSet

router = routers.DefaultRouter()
router.register(prefix='user', viewset=UserViewSet, basename='user_api')
router.register(prefix='trainer', viewset=TrainerViewSet, basename='trainer_api')
router.register(prefix='student', viewset=StudentViewSet, basename='student_api')

urlpatterns = router.urls
