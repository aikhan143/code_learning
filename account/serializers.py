from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)
    class Meta:
        model = User
        fields = 'password', 'password_confirm', 'email'
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password_confirm == password:
            return attrs
        raise ValueError ('Пароли должны совпадать')
    
    def create(self, **data):
        user = User.objects.create_user(**data)
        