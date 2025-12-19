from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(AppUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_staff', 'is_active']


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'code']
