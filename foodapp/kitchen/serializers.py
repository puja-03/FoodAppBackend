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
    logo = serializers.ImageField(required=False, allow_null=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)

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

class MenuQuantitySerializer(serializers.ModelSerializer):
    menu = serializers.IntegerField(source='menu.id', read_only=True)
    class Meta:
        model = MenuQuantity
        fields = "__all__"

class MenuSerializer(serializers.ModelSerializer):
    quantities = MenuQuantitySerializer(many=True)
    class Meta:
        model = Menu
        fields = "__all__"

    def create(self, validated_data):
        quantities_data = validated_data.pop('quantities')
        menu = Menu.objects.create(**validated_data)
        for qty_data in quantities_data:
            MenuQuantity.objects.create(menu=menu, **qty_data)
        return menu

    def update(self, instance, validated_data):
        quantities_data = validated_data.pop('quantities', None)

        # Update menu fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If quantities provided, update them
        if quantities_data is not None:
            instance.quantities.all().delete()
            for qty_data in quantities_data:
                MenuQuantity.objects.create(menu=instance, **qty_data)

        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value.strip()

class ThaliSerializer(serializers.ModelSerializer):
    # kitchen = KitchenProfileSerializer(read_only=True)
    toppings = ToppingSerializer(many=True, read_only=True)
    topping_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Thali
        fields = ['id','title', 'description', 'price', 
                 'preparation_time', 'image', 'calories', 'is_available', 
                 'toppings', 'topping_ids', 'rating']
        read_only_fields = ['kitchen']

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value.strip()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_topping_ids(self, value):
        if value:
            existing_ids = set(Topping.objects.filter(id__in=value).values_list('id', flat=True))
            invalid_ids = set(value) - existing_ids
            if invalid_ids:
                raise serializers.ValidationError(f"Invalid topping IDs: {invalid_ids}")
        return value

    def create(self, validated_data):
        topping_ids = validated_data.pop('topping_ids', [])
        thali = Thali.objects.create(**validated_data)
        if topping_ids:
            thali.toppings.set(topping_ids)
        return thali

    def update(self, instance, validated_data):
        if 'topping_ids' in validated_data:
            topping_ids = validated_data.pop('topping_ids')
            instance.toppings.set(topping_ids)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['toppings'] = ToppingSerializer(instance.toppings.all(), many=True).data
        return representation
