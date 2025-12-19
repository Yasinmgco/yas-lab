import time

from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from send_email.send_email import *


# Create your views here.

class UserAPIView(generics.ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    RATE_LIMIT_SECONDS = 60

    def post(self, request):
        serializer = GetEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if not email:
                return Response({'error': 'email is required'}, status=400)

            cooldown_key = f'sms_cooldown_{email}'
            last_sent = cache.get(cooldown_key)
            if last_sent:
                seconds_left = int(self.RATE_LIMIT_SECONDS - (time.time() - last_sent))
                if seconds_left > 0:
                    return Response(
                        {'error': f'لطفاً {seconds_left} ثانیه صبر کنید'},
                        status=429
                    )

            OTP.objects.filter(email=email).delete()
            code = OTP.generate_code()
            OTP.objects.create(email=email, code=code)
            cache.set(cooldown_key, time.time(), timeout=self.RATE_LIMIT_SECONDS)

            send_otp_mail(code, email)

            return Response({'message': 'کد تایید به ایمیل شما ارسال شد'}, status=200)

        return Response(serializer.errors, status=400)


class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp_serializer = OTPVerifySerializer(data=request.data)
        if otp_serializer.is_valid():
            code = otp_serializer.validated_data['code']
            otp = OTP.objects.filter(code=code).last()
            if not otp or not otp.is_valid():
                return Response({"error": "کد تایید اشتباه یا منقضی شده"}, status=400)

            user, created = AppUser.objects.get_or_create(email=otp.email)

            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response({'error': 'Invalid email!'})


class SetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()
            return Response(
                {'message': 'signup successfully!'}, status=200
            )
        return Response(serializer.errors, status=400)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if not user:
                return Response({'message': 'email or password is incorrect.'}, status=400)

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'login successfully!',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=200)
        return Response(serializer.errors, status=400)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()

            return Response({'message': 'logout successfully'}, status=200)
        except Exception:
            return Response({'message': 'Invalid refresh token'}, status=400)


class ForgetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    RATE_LIMIT_SECONDS = 60

    def post(self, request):
        serializer = GetEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if not email:
                return Response({'error': 'email is required'}, status=400)

            cooldown_key = f'sms_cooldown_{email}'
            last_sent = cache.get(cooldown_key)
            if last_sent:
                seconds_left = int(self.RATE_LIMIT_SECONDS - (time.time() - last_sent))
                if seconds_left > 0:
                    return Response(
                        {'error': f'لطفاً {seconds_left} ثانیه صبر کنید'},
                        status=429
                    )

            OTP.objects.filter(email=email).delete()
            code = OTP.generate_code()
            OTP.objects.create(email=email, code=code)
            cache.set(cooldown_key, time.time(), timeout=self.RATE_LIMIT_SECONDS)

            send_reset_password_code_mail(code, email)

            return Response({'message': 'کد به ایمیل شما ارسال شد'}, status=200)
        return Response(serializer.errors, status=400)


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')

            otp = OTP.objects.filter(code=code).last()
            if not otp or not otp.is_valid():
                return Response({"error": "کد تایید اشتباه یا منقضی شده"}, status=400)

            email = otp.email
            try:
                user = AppUser.objects.get(email=email)
            except AppUser.DoesNotExist:
                return Response({'message': 'user not found!'}, status=400)
            user.set_password(serializer.validated_data.get('password'))
            user.save()

            otp.delete()

            return Response({'message': 'رمز شما با موفقیت ریست شد.'}, status=200)
        return Response(serializer.errors, status=400)
