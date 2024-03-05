from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns =[
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', TokenObtainPairView.as_view(), name='TokenObtain'),
    path('refresh/', TokenRefreshView.as_view(), name='TokenRefresh'),
    path('activate/<str:email>/<str:activation_code>/', ActivateView.as_view(), name='activate')
]