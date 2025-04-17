from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'pincode', 'profile_image', 'created_at']
   
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','thali','quantity',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user',
        'delivery_address',
        'total_price',
        'payment_method',
        'payment_status',
        'order_status'
    )

@admin.register(OrderItem)  
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'thali', 'quantity', 'price')
    readonly_fields = ('created_at', 'updated_at')

# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'thali')