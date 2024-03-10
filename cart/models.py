from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project
from django.utils.crypto import get_random_string


User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    projects = models.ManyToManyField(Project, through='CartProject', related_name='projects')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(project.total_price() for project in self.cart_projects.all())

    def clear_cart(self):
        self.projects.clear()

    def __str__(self):
        return f"Cart #{self.id} - User: {self.user.name}"

class CartProject(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cart_projects')
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.project.price * self.quantity

    def __str__(self):
        return f"{self.quantity} - {self.project.title}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='orders', null=True, blank=True, unique=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    verification_code = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='Payment Intent ID')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} with the total price {self.total_price} - User: {self.user.name}."
    
    def create_verification_code(self):
        code = get_random_string(10)
        self.verification_code = code 
        self.save()