from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
import random


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError('Superusers must have a password')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('MALE', 'مرد'),
        ('FEMALE', 'زن')
    )

    email = models.EmailField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=25, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(blank=True, null=True)
    referral_id = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='media/user_image', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class OTP(models.Model):
    objects = models.Manager()

    code = models.CharField(max_length=5)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=2)

    @staticmethod
    def generate_code():
        return str(random.randint(10000, 99999))
