from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from projects.serializers import ProjectSerializer, ProjectListSerializer
from .tasks import *

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
    cart = serializers.ReadOnlyField(source='cart.id')
    total_price = serializers.ReadOnlyField(source='cart.total_price')

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'created_at', 'cart']

    def create(self, validated_data):
        user = self.context.get('request').user
        cart_id = self.context['view'].kwargs.get('id')

        cart = get_object_or_404(Cart, id=cart_id)
        
        if cart.projects.exists():

            total_price = cart.total_price()

            order = Order.objects.create(user=user, cart=cart, total_price=total_price, **validated_data)
            send_order_details(user.email, order, order.verification_code)
            order.save()
            return order
        else:
            raise serializers.ValidationError('Cart is empty')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['projects'] = ProjectListSerializer(instance.cart.projects.all(), many=True).data
        return representation
    
class VerificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'verification_code']

    def validate(self, attrs):
        user = attrs.get('user')
        code = attrs.get('verification_code')

        if not Order.objects.filter(user=user, verification_code=code).exists(): 
            raise serializers.ValidationError('Order not found')
        return attrs
    
    def verify(self):
        user = self.validated_data.get('user')
        order = Order.objects.get(user=user, is_verified=False)
        order.is_verified = True
        order.verification_code = ''
        order.save()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['payment_link'] = self.create_payment_link()
        return representation
