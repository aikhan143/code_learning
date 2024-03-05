from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('activate/', ActivateView.as_view()),
    path('ForgotPassword/', ForgotPasswordView.as_view()),
    path('ForgotPasswordSolution/', ForgotPasswordSolutionView.as_view()),
    path('ChangePassword/', ChangePasswordView.as_view())
]
