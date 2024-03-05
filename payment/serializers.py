from rest_framework import serializers
import os
from dotenv import load_dotenv
import stripe
from .models import *

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class PaymentSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Payment
        fields = '__all__'

    def create_payment_link(self, course):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': course.title,
                            'description': course.description,
                        },
                        'unit_amount': course.price,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel'
            )

            return session.url

        except stripe.error.StripeError as e:
            return f'Error: {str(e)}'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user
        course = validated_data.get('course')
        payment_link = self.create_payment_link(course)

        payment = Payment.objects.create(user=user, course=course, **validated_data)

        return payment

     