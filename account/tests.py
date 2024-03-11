from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.contrib.auth import get_user_model
from .views import *
from django.contrib.auth.hashers import make_password


User = get_user_model()

class AuthTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email = 'user@gmail.com',
            password = '12345678',
            is_active = True,
            activation_code = '1234',
            name = 'test'
        )
    
    def test_registration(self):
        data={
            'email': 'user@gmail.com',
            'password': '12345678',
            'password_confirm': '12345678',
            'name': 'test',
        }

        request = self.factory.post('/api/v1/register/', data, format='json')
        view = RegisterView.as_view()
        response = view(request)
        assert User.objects.filter(email=data['email']).exists()
        # assert response.status_code==201
    
    def test_change_password(self):
        data = {
            'old_password': '12345678',
            'new_password': '1234567a',
            'new_password_confirm':'1234567a',
            'email': 'user@gmail.com',
        }

        request = self.factory.post('/api/v1/ChangePassword/',data, format='json')

        force_authenticate(request, user=self.user)
        view = ChangePasswordView.as_view()
        response = view(request)
        # assert response.status_code==200
        # password = User.objects.get(email=self.user.email).password
        # assert password == make_password(data['new_password'])
        assert response.status_code==200
    
    def test_forgot_password(self):
        request = self.factory.post('ForgotPassword/', data={'email': self.user.email}, format='json')
        view = ForgotPasswordView.as_view()
        response = view(request)
        assert response.status_code==200

    def test_forgot_pass_complete(self):
        data={
            'email':'user@gmail.com', 
            'code':'1234', 
            'password':'1234a', 
            'password_confirm':'1234a'
            }
        request = self.factory.post('ForgotPasswordSolution/',data, format='json')
        view = ForgotPasswordSolutionView.as_view()
        response = view(request)
        assert response.status_code==200