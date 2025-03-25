from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'pincode', 'profile_image', 'created_at']