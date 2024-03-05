from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

class RegisterView(APIView):
    def post(self, request):
        user_request = RegisterSerializer(data=request.data)
        user_request.is_valid(raise_exception=True)
        user_request.save()
        return Response(user_request.data, status=201)
    
class ActivateView(APIView):
    def post(self, request):
        user_request = ActivateSerializer(data=request.data)
        if user_request.is_valid(raise_exception=True):
            user_request.activate()
            return Response('Аккаунт успешно активирован', status=200
            )
        
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        deleted = Token.objects.filter(user=user).delete()
        if deleted:
            return Response(f'Вы вышли из аккаунта {user.email}')
        else:
            return Response('Вы ввели неправильные данные')

class ForgotPasswordView(APIView):
    def post(self, request):
        user_request = ForgotPasswordSerializer(data=request.data) 
        user_request.is_valid(raise_exception=True)
        user_request.send_verification_email()
        return Response ('Вам был отправлен смс код на вашу почту', status = 200)
    
class ForgotPasswordSolutionView(APIView):
    def post(self, request):
        user_request = ForgotPasswordSolutionSerializer(data=request.data)
        user_request.is_valid(raise_exception=True)
        user_request.create_new_password()
        return Response ('Ваш код успешно восстановлен')
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user_request = ChangePasswordSerializer(data=request.data, context ={'request': request})
        user_request.is_valid(raise_exception=True)
        user_request.create_new_password()
        return Response('Пароль успешно изменён', status=200)

