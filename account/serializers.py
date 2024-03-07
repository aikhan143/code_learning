from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.mail import send_mail
from .models import CustomUser
from .tasks import send_activation_code, send_verification_email

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(min_length=8, max_length=20, required=True)
    password_confirm = serializers.CharField(required = True, write_only=True)
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(read_only=True)

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        except:
            return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password == password_confirm:
            return attrs
        raise serializers.ValidationError('Пароли не совпадают')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user

    

class ActivateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if User.objects.filter(email=email, activation_code=code).exists(): 
            return attrs
        else:
            raise serializers.ValidationError('Неправильный email или код активации')
        
    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()

    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, email):
        if User.objects.get(email=email):
            return email
        raise serializers.ValidationError ('Пользователь не существует')
    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_verification_email(user.email, user.activation_code)
    
class ForgotPasswordSolutionSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if User.objects.filter(email=email, activation_code=code).exists() and password == password_confirm:
            return attrs
        else:
            raise serializers.ValidationError('Неверный пароль или код')
    
    def create_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_email(self, email):
        if User.objects.get(email=email):
            return email
        raise serializers.ValidationError ('Пользователь не существует')
    
    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if user.check_password(old_password):
            return old_password
        raise serializers.ValidationError ('Неверный пароль')
    
    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        if new_password == old_password:
            raise serializers.ValidationError('Старый и новый пароль не может быть похожим')
        return attrs
    
    def create_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()

        