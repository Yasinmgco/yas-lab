from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('users/', views.UserAPIView.as_view(), name='user_api'),
    path('send-otp/', views.RegisterAPIView.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyCodeAPIView.as_view(), name='verify_otp'),
    path('set-pass/', views.SetPasswordAPIView.as_view(), name='set_password'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('forget-pass/', views.ForgetPasswordAPIView.as_view(), name='forget_password'),
    path('reset-pass/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
]
