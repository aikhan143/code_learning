from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    def create_user_manager(self, email,password, **extra):
        if not email:
            raise ValueError('Поле email объязателен к вводу!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, **extra):
        user = self.create_user_manager(email, password, **extra)
        user.create_activation_code()
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_active', True)
        return self.create_user_manager(email, password, **extra)
        
    
class User(AbstractUser):
    username = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    activation_code = models.CharField(max_legth=8, blank=True)
    is_active = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)


    USERNAME_FIELD = email

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
    def create_activation_code(self):
        code = get_random_string(length=8, allowed_chars='abcdEfghijklmnopwyz0123456789')
        self.activation_code = code




    