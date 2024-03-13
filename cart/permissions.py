from rest_framework.permissions import BasePermission 
from .models import Order, CartProject

class IsPaidPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        paid_order_exists = Order.objects.filter(user=user, is_paid=True).exists()
        if not paid_order_exists:
            return False

        paid_order = Order.objects.get(user=user, is_paid=True)

        cart_project = CartProject.objects.filter(cart__user=user, project__in=paid_order.cart.projects.all()).first()

        return cart_project is not None