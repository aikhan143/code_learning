from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_save
import stripe
import os
from .models import *
from projects.serializers import ProjectSerializer, ProjectListSerializer
from .tasks import *

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class CartProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProject
        fields = ['project', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Cart
        fields = ['user', 'projects', 'total_price']


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created and not Cart.objects.filter(user=instance).exists():
        Cart.objects.create(user=instance)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    total_price = serializers.ReadOnlyField(source='cart.total_price')

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        cart = user.cart.first()
        validated_data['user'] = user

        if cart.projects.exists():
            total_price = cart.total_price() 
            order = Order.objects.create(user=user, cart=cart, total_price=total_price)
            order.create_verification_code()
            send_order_details(user.email, order, order.verification_code)
            order.save()
            return order
        raise serializers.ValidationError('Cart is empty')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['projects'] = ProjectListSerializer(instance.cart.projects.all(), many=True).data
        return representation
        
class VerificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Order
        fields = ['id', 'user', 'verification_code']

    def create_payment_link(self):
        user = self.context.get('request').user
        cart = user.cart.first()
        project = cart.projects.first()
        order_pk = self.context['view'].kwargs.get('pk')
        order = Order.objects.get(pk=order_pk, user=user)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': project.title,
                            'description': project.description,
                        },
                        'unit_amount': int(project.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel'
            )

            payment_intent_id = session.payment_intent
            order.payment_intent_id = payment_intent_id
            order.save()

            return session.url

        except stripe.error.StripeError as e:
            raise serializers.ValidationError(f'Error: {str(e)}')


    def create(self, validated_data):
        user = self.context.get('request').user
        code = validated_data.get('verification_code')
        order_pk = self.context['view'].kwargs.get('pk')

        try:
            order = Order.objects.get(pk=order_pk, user=user, verification_code=code, is_verified=False)
            order.is_verified = True
            order.verification_code = ''
            order.save()
        except Order.DoesNotExist:
            print(f"Order not found. Order ID: {order_pk}, User ID: {user.id}, Verification Code: {code}")
            raise serializers.ValidationError('Order not found')

        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['payment_link'] = self.create_payment_link()
        return representation
