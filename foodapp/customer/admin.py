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


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_thali_name', 'created_at')
    readonly_fields = ('created_at',)

    def get_thali_name(self, obj):
        return obj.thali.name
    get_thali_name.short_description = 'Thali Name'

