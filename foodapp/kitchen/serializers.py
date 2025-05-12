from rest_framework import serializers
from kitchen.models import *
from rest_framework.permissions import IsAuthenticated
from userapp.auth_serializer import UserSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role"]  

class OwnerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    class Meta:
        model = Owner
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = CustomUserSerializer(instance.user).data
        return representation
class KitchenProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenProfile
        fields = [
            'id', 'title', 'tag', 'rating', 'reviews_count',
            'preparation_time', 'logo', 'cover_image', 'is_active'
        ]
        read_only_fields = ['rating', 'reviews_count']

    def validate_logo(self, value):
        if value and value.size > 2 * 1024 * 1024:  # 2MB limit
            raise serializers.ValidationError("Logo file size cannot exceed 2MB")
        return value

    def validate_cover_image(self, value):
        if value and value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("Cover image file size cannot exceed 5MB")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = CustomUserSerializer(instance.user).data
        return representation

    def create(self, validated_data):
        user = self.context['request'].user
        return KitchenProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

# class MenuQuantitySerializer(serializers.ModelSerializer):
#     menu = serializers.IntegerField(source='menu.id', read_only=True)
#     class Meta:
#         model = MenuQuantity
#         fields = "__all__"

# class MenuSerializer(serializers.ModelSerializer):
#     quantities = MenuQuantitySerializer(many=True)
#     class Meta:
#         model = Menu
#         fields = "__all__"

#     def create(self, validated_data):
#         quantities_data = validated_data.pop('quantities')
#         menu = Menu.objects.create(**validated_data)
#         for qty_data in quantities_data:
#             MenuQuantity.objects.create(menu=menu, **qty_data)
#         return menu

#     def update(self, instance, validated_data):
#         quantities_data = validated_data.pop('quantities', None)

#         # Update menu fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         # If quantities provided, update them
#         if quantities_data is not None:
#             instance.quantities.all().delete()
#             for qty_data in quantities_data:
#                 MenuQuantity.objects.create(menu=instance, **qty_data)

#         return instance

# class ToppingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Topping
#         fields = "__all__"
#         read_only_fields = ['created_at', 'updated_at']

#     def validate_name(self, value):
#         if len(value.strip()) < 3:
#             raise serializers.ValidationError("Name must be at least 3 characters long")
#         return value.strip()

# class ThaliSerializer(serializers.ModelSerializer):
#     kitchen = KitchenProfileSerializer(read_only=True)
#     toppings = serializers.ListField(
#         child=serializers.CharField(),
#         write_only=True,
#         required=False
#     )
#     topping_details = ToppingSerializer(source='toppings', many=True, read_only=True)

#     class Meta:
#         model = Thali
#         fields = ['id','kitchen','title', 'description', 'price', 
#                  'preparation_time', 'image', 'calories', 'is_available', 
#                  'toppings', 'topping_details', 'rating']
#         read_only_fields = ['kitchen']

#     def validate_title(self, value):
#         if len(value.strip()) < 3:
#             raise serializers.ValidationError("Title must be at least 3 characters long")
#         return value.strip()

#     def validate_price(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Price must be greater than 0")
#         return value

#     def _get_or_validate_toppings(self, topping_names):
#         topping_objects = []
#         invalid_toppings = []

#         for name in topping_names:
#             name = name.strip()
#             toppings = Topping.objects.filter(name__iexact=name)
            
#             if not toppings.exists():
#                 invalid_toppings.append(name)
#             else:
#                 # Get the first matching topping
#                 topping_objects.append(toppings.first())

#         if invalid_toppings:
#             raise serializers.ValidationError(
#                 f"Following toppings do not exist: {', '.join(invalid_toppings)}"
#             )
#         return topping_objects

#     def create(self, validated_data):
#         topping_names = validated_data.pop('toppings', [])
#         thali = Thali.objects.create(**validated_data)
#        # toppping add by name
#         for name in topping_names:
#             try:
#                 topping = Topping.objects.get(name__iexact=name.strip())
#                 thali.toppings.add(topping)
#             except Topping.DoesNotExist:
#                 raise serializers.ValidationError(f"Topping '{name}' does not exist")

#         return thali

#     def update(self, instance, validated_data):
#         topping_names = validated_data.pop('toppings', None)
        
#         # Update other fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
        
#         # Update toppings if provided
#         if topping_names is not None:
#             instance.toppings.clear()
#             for name in topping_names:
#                 try:
#                     topping = Topping.objects.get(name__iexact=name.strip())
#                     instance.toppings.add(topping)
#                 except Topping.DoesNotExist:
#                     raise serializers.ValidationError(f"Topping '{name}' does not exist")
        
#         instance.save()
#         return instance

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['toppings'] = ToppingSerializer(instance.toppings.all(), many=True).data
#         return representation

class SubItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubItem
        fields = ['id', 'title', 'cost', 'image', 'subitem_type']

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id','kitchen', 'title', 'code', 'created_at', 'updated_at']

    
class ThaliSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thali
        fields = [
            'id', 'kitchen', 'title', 'description', 'price', 'rating',
            'preparation_time', 'image','special', 'thali_offer',
            'main_courses', 'starters', 'desserts','is_available', 'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subitem'] = SubItemSerializer(instance.subitem).data
        return representation
   