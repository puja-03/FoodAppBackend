from .models import *
from rest_framework import serializers
from userapp.auth_serializer import *
from userapp.auth_serializer import UserSerializer
from kitchen.serializers import ThaliSerializer


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
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price','delivery_address', 
                 'order_status', 'payment_method', 'created_at']
        read_only_fields = ['user', 'total_price', 'order_status']
    
    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = CartItem.objects.filter(user=user)
        
        if not cart_items.exists():
            raise serializers.ValidationError({"error": "Cart is empty"})

        # Calculate total price from cart items including toppings
        total_price = sum(item.get_total_price() for item in cart_items)

        # Create order
        order = Order.objects.create(
            user=user,
            delivery_address=validated_data.get('delivery_address'),
            payment_method=validated_data.get('payment_method'),
            total_price=total_price,
            order_status='PENDING'
        )
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                thali=cart_item.thali,
                quantity=cart_item.quantity,
                price=cart_item.get_total_price()
            )

        # Clear cart
        cart_items.delete()

        return order
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ['id', 'thali', 'created_at']
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['thali'] = ThaliSerializer(instance.thali, many=True).data
        return representation
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'thali', 'quantity', 'price']

