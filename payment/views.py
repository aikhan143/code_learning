# from rest_framework.views import APIView
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.response import Response

# import stripe
# from .serializers import *

# stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# class PaymentView(APIView):
#     def get(self, request, *args, **kwargs):
#         order_id = kwargs.get('id')
#         order = Course.objects.get(slug=order_id)
#         payment_link = self.create_payment_link(order)

#         serializer = PaymentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({'payment_link': payment_link})
    
#     @csrf_exempt
#     def stripe_webhook(request):
#         payload = request.body
#         sig_header = request.headers.get('Stripe-Signature')

#         endpoint_secret = os.environ.get('STRIPE_WEBHOOK_KEY')

#         event = None

#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header, endpoint_secret
#             )
#         except ValueError as e:
#             return Response(status=400)
#         except stripe.error.SignatureVerificationError as e:
#             return Response(status=400)

#         if event['type'] == 'payment_intent.succeeded':
#                 payment_intent_id = event['data']['object']['id']
#         try:
#             transaction = Payment.objects.get(payment_intent_id=payment_intent_id)
#             transaction.is_paid = True
#         except Payment.DoesNotExist:
#             return Response({'error': 'Transaction not found'}, status=404)

#         return Response(status=200)