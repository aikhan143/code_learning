from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_activation_code(email, activation_code):
    message = f'''Вы успешно зарегестрировались, используйте этот код для активации аккаунта {activation_code}'''
    send_mail(
        subject = 'Активация аккаунта',
        message = message,
        from_email = 'marovmalik83@gmail.com',
        recipient_list = [email]
    )