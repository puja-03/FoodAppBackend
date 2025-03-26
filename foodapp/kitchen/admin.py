from django.contrib import admin
from .models import *

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'address', 'pincode','user', 'city', 'state', 'gst_number', 'profile_image')

@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner','description','address', 'city', 'state','pincode' ,'logo','cover_image','status')

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('kitchen', 'bank_name', 'account_holder_name', 'account_number', 'ifsc_code', 'upi_id')
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('Item_name', 'Category', 'Image', 'Description','Prep_Time')

