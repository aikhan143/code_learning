# from rest_framework import serializers
# from django.shortcuts import get_object_or_404
# import os
# from dotenv import load_dotenv
# import stripe
# from .models import *

# load_dotenv()

# stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# class PaymentSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.name')
#     project = serializers.ReadOnlyField(source='project.title')

#     class Meta:
#         model = Payment
#         fields = '__all__'

#     def create_payment_link(self, project):
#         try:
#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=[{
#                     'price_data': {
#                         'currency': 'usd',
#                         'product_data': {
#                             'name': project.title,
#                             'description': project.description,
#                         },
#                         'unit_amount': project.price,
#                     },
#                     'quantity': 1,
#                 }],
#                 mode='payment',
#                 success_url='https://example.com/success',
#                 cancel_url='https://example.com/cancel'
#             )

#             return session.url

#         except stripe.error.StripeError as e:
#             raise serializers.ValidationError(f'Error: {str(e)}')

#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         validated_data['user'] = user
#         project_slug = self.context['view'].kwargs.get('slug')

#         project = get_object_or_404(Project, slug=project_slug)

#         validated_data['project'] = project
#         payment_link = self.create_payment_link(project)

#         payment = Payment.objects.create(user=user, project=project, **validated_data)

#         return payment

     