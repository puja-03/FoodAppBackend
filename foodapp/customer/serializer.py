from .models import *
from rest_framework import serializers
from userapp.auth_serializer import *
from userapp.auth_serializer import UserSerializer
from kitchen.serializers import ToppingSerializer,ThaliSerializer 


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    pincode = serializers.CharField(max_length=15, required=False, allow_blank=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'address', 'city','state','pincode','profile_image', 'created_at']

    def validate_user(self, value):
        if value.role != 'customer':
            raise serializers.ValidationError("User is not a customer")
        return value
    
    def validate_pincode(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError("pincode should contain only numbers")
        if len(value) < 6:
            raise serializers.ValidationError("pincode should be atleast 6 characters long")
        if len(value) > 6:
            raise serializers.ValidationError("pincode should be atmost 6 characters long")
        return value
        

class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'thali', 'quantity','created_at', 'updated_at']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    
    def create(self, validated_data):
        if 'thali' not in validated_data:
            raise serializers.ValidationError("Thali is required.")
        return super().create(validated_data)


    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['user'] = UserSerializer(instance.user).data
    #     representation['thali'] = ThaliSerializer(instance.user).data
    #     return representation


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    cart_items = CartItemSerializer(many=True, read_only=True)
    delivery_address = serializers.CharField(required=True)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, required=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart_items', 'total_price', 'payment_method',
                 'payment_status', 'order_status', 'delivery_address',
                 'created_at', 'updated_at']
        read_only_fields = ['payment_status', 'order_status']

    def validate_total_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total price must be greater than zero.")
        return value

    def validate_delivery_address(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Delivery address must be at least 10 characters long.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['cart_items'] = CartItemSerializer(instance.cart_items, many=True).data
        representation['delivery_address'] = CustomerSerializer(instance.delivery_address).data
        return representation

    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty")
        
        total_price = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            **validated_data
        )
        order.cart_items.set(cart_items)
        return order
        
class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    cart = CartItemSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'cart', 'created_at']
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['cart'] = CartItemSerializer(instance.cart).data
        return representation