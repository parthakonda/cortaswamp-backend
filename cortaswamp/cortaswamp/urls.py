from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from authentication.rest.viewsets import signup, CheckResetPasswordView, ResetPasswordView, ForgotPasswordView

urlpatterns = [
    path('api-token-auth/', obtain_jwt_token),
    path('signup/', signup),
    path(
        'forgot-password/',
        ForgotPasswordView.as_view(),
        name='forgot-password'),
    path(
        'check-password/<id>/',
        CheckResetPasswordView.as_view(),
        name='check-password'),
    path(
        'reset-password/<id>/',
        ResetPasswordView.as_view(),
        name='reset-password'),
]
