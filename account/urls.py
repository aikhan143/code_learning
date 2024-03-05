from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/', ActivateView.as_view()),
    path('ForgotPassword/', ForgotPasswordView.as_view()),
    path('ForgotPasswordSolution/', ForgotPasswordSolutionView.as_view()),
    path('ChangePassword/', ChangePasswordView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
