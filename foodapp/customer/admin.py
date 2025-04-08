from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'pincode', 'profile_image', 'created_at']
   

@admin.register(Thali)
class ThaliAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_toppings', 'calories', 'estimated_time', 'created_at')
    filter_horizontal = ('toppings',)  # For better m2m field handling in edit form
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'toppings')

    def get_toppings(self, obj):
        return ", ".join([topping.name for topping in obj.toppings.all()])
    get_toppings.short_description = 'Toppings'
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'get_thali_name', 'quantity', 'get_total_price')
    readonly_fields = ('created_at', 'updated_at')

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'

    def get_thali_name(self, obj):
        return obj.thali.name
    get_thali_name.short_description = 'Thali Name'

    def get_total_price(self, obj):
        return f"₹{obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'get_user_email',
        'total_price',
        'payment_method',
        'payment_status',
        'order_status'
    )
    list_filter = ('order_status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('user__email', 'delivery_address')
    readonly_fields = ('created_at', 'updated_at', 'cart_items')
    filter_horizontal = ('cart_items',)

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'cart_items', 'total_price')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Order Status', {
            'fields': ('order_status',)
        }),
        ('Delivery Information', {
            'fields': ('delivery_address',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
