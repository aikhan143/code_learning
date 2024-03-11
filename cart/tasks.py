from django.core.mail import send_mail
from config.celery import app
from rest_framework.response import Response
from .models import Order

@app.task
def send_order_details(email, order, verification_code):
    message = f'''You have placed an order on out platform. You order: {order}. Please send this code to verify your order: {verification_code}
    '''
    send_mail(
        'Order details',
        message,
        'test@gmail.com',
        [email]
    )

@app.task
def handle_payment_intent_succeeded(payment_intent_id):
    try:
        order = Order.objects.get(payment_intent_id=payment_intent_id)
        order.is_paid = True
        order.save()
        print('Payment intent succeeded for Order ID:', order.id)
    except Order.DoesNotExist:
        print('Order not found for Payment Intent ID:', payment_intent_id)
