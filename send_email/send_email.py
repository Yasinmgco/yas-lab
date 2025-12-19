from django.core.mail import send_mail
from Yaslang import settings


def send_otp_mail(code, receivers):
    send_mail('verify your email.',
              f'your code:{code}',
              settings.EMAIL_HOST_USER,
              [receivers],
              fail_silently=True)

def send_reset_password_code_mail(code, receivers):
    send_mail('verify your email.',
              f'your reset password code is:{code}',
              settings.EMAIL_HOST_USER,
              [receivers],
              fail_silently=True)

