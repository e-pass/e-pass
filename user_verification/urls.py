from django.urls import path
from rest_framework import routers

from user_verification.views import (SendConfirmationCodeView,
                                     VerifyConfirmationCode)

router = routers.DefaultRouter()
router.register(prefix=r'auth/verify-code',
                viewset=VerifyConfirmationCode,
                basename='verify_confirmation_code')

urlpatterns = [
    path(r'auth/send-code/', SendConfirmationCodeView.as_view())
] + router.urls
