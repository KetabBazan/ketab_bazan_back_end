from django.urls import path, include
from .views import ResetPassword, ResetPasswordConfirm
urlpatterns = [
    path('', ResetPassword.as_view()),
    path('confirm/', ResetPasswordConfirm.as_view())
]