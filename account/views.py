from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class RegisterView(APIView):
    def post(self, request):
        user_request = RegisterSerializer(data=request.data)
        user_request.is_valid(raise_exception=True)
        user_request.save()
        return Response('Спасибо за регестрацию', status=201)
    
class ActivateView(APIView):
    def post(self, request):
        user_request = ActivateSerializer(data=request.data)
        if user_request.is_valid(raise_exception=True):
            user_request.activate()
            return Response('Аккаунт успешно активирован', status=200
            )

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

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data['refresh_token']
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"message": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": "Не удалось выполнить выход из системы."}, status=status.HTTP_400_BAD_REQUEST)


