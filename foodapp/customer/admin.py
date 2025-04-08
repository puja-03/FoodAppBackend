from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'pincode', 'profile_image', 'created_at']
    search_fields = ('user__email', 'user__name', 'address')
    list_filter = ('created_at',)

@admin.register(Thali)
class ThaliAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','toppings','description', 'calories', 'estimated_time', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'thali', 'quantity', 'get_total_price', 'created_at')

    def get_total_price(self, obj):
        return f"₹{obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'total_price', 'payment_method', 'cart_items',
        'payment_status', 'order_status', 'created_at'
    )
   
