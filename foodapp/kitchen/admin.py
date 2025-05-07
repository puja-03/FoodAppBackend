from django.contrib import admin
from .models import *

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'address', 'pincode','user', 'city', 'state', 'gst_number', 'profile_image')

@admin.register(KitchenProfile)
class KitchenAdmin(admin.ModelAdmin):
    list_display = ('user', 'title','tag','rating', 'reviews_count', 'preparation_time','logo','cover_image','is_active')

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('kitchen', 'bank_name', 'account_holder_name', 'account_number', 'ifsc_code', 'upi_id')
# @admin.register(Menu)
# class MenuAdmin(admin.ModelAdmin):
#     list_display = ('item_name', 'category', 'Image', 'description','prep_Time','Isavailable')

# @admin.register(MenuQuantity)
# class MenuQuantity(admin.ModelAdmin):
#     list_display = ("menu_id", "quantity", 'quantity_type' ,'price')
# @admin.register(Topping)
# class ToppingAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description','price' ,'image', 'created_at', 'updated_at')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('kitchen', 'title', 'code', 'created_at', 'updated_at')

@admin.register(SubItem)
class SubItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost','subitem_type', 'image')

@admin.register(Thali)  
class ThaliAdmin(admin.ModelAdmin):
    list_display = ('kitchen', 'title', 'description', 'price', 'rating', 'preparation_time', 
                   'image', 'type', 'special', 'thali_offer', 'is_available', 
                   'created_at', 'updated_at')
    
# @admin.register(Thali)
# class ThaliAdmin(admin.ModelAdmin):
#     list_display = ('title','kitchen','description', 'price', 'get_toppings', 'preparation_time', 
#                    'image', 'is_available', 'created_at', 'updated_at')

#     def get_toppings(self, obj):
#         return ", ".join([topping.name for topping in obj.toppings.all()])
#     get_toppings.short_description = 'Toppings'

