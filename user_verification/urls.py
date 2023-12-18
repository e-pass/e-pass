from rest_framework import routers

from user_verification.views import (SendConfirmationCodeView,
                                     VerifyConfirmationCode)

router = routers.DefaultRouter()
router.register(prefix=r'auth/send-code',
                viewset=SendConfirmationCodeView,
                basename='send_confirmation_code')
router.register(prefix=r'auth/verify-code',
                viewset=VerifyConfirmationCode,
                basename='verify_confirmation_code')

urlpatterns = router.urls
