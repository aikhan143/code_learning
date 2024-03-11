from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')

urlpatterns = [
    path('cart/<int:pk>/', CartViewSet.as_view({'get': 'retrieve'}), name='cart-get'),
    path('projects/<slug:pk>/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='cart-add-to-cart'),
    path('order/verify-order/<int:pk>/', VerificationView.as_view()),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
]

urlpatterns += router.urls