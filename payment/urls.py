from django.urls import path
from .views import PaymentView

urlpatterns = [
    path('courses/<slug:course_slug>/pay/', PaymentView.as_view(), name='payment-view'),
    path('stripe/webhook/', PaymentView.stripe_webhook, name='stripe-webhook'),
]