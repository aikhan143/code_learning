from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse
import stripe

from .models import *
from projects.models import Project
from .serializers import *
from review.permissions import IsAuthorPermission

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user).order_by('updated_at')
        return queryset
    
    def get_permissions(self):
        if self.action == ['create']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        user = request.user
        project = Project.objects.get(slug=pk)
        
        cart = Cart.objects.get(user=user)
        if cart.user != user:
            return Response('You do not have permission to perform this action.', status=403)

        cart_project, project_created = CartProject.objects.get_or_create(cart=cart, project=project)

        if not project_created:
            cart_project.quantity += 1
            cart_project.save()

        serializer = CartProjectSerializer(cart_project)
        return Response(serializer.data, status=201)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthorPermission]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user).order_by('created_at')
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.cart.clear_cart()
        instance.delete()
        return Response('Order canceled successfully', status=204)
        
class VerificationView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = VerificationSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
        json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = getattr(event.data, 'object', None)
        if payment_intent:
            payment_intent_id = event['data']['object']['id']
            print(payment_intent_id)
            handle_payment_intent_succeeded.delay(payment_intent_id)
            print('PaymentIntent was successful!')
    elif event.type == 'payment_method.attached':
        payment_method = getattr(event.data, 'object', None)
        if payment_method:
            print('PaymentMethod was attached to a Customer!')
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
