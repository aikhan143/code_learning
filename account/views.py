from rest_framework.views import APIView
from .serializers import*
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Аккоунт зарегестрирован')
    
class ActivateView(APIView):
    def post(self, email, activation_code):
        user = get_user_model().objects.filter(email=email, activation_code=activation_code).first()
        if user:
            user.activation_code = ''
            user.is_active=True
            user.save()
            return Response('Аккаунт успешно активирован', status=200)
        return Response ('Аккаунт не найден', status=400)

# Create your views here.
