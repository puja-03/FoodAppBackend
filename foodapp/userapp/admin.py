from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'role', 'is_active', 'is_verified', 'is_staff', 'otp', 'otp_created_at']