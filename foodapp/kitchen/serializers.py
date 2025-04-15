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
    owner = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all()) 
    class Meta:
        model = KitchenProfile
        fields = "__all__"

    # def to_representation(self, instance):class ThaliViewSet(viewsets.ModelViewSet):
    queryset = Thali.objects.all()  # Add default queryset
    permission_classes = [IsAuthenticated]
    # serializer_class = ThaliSerializer

    def get_queryset(self):
        # Filter thalis for current user and handle search
        queryset = Thali.objects.filter(user=self.request.user)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            price = float(request.data.get('price', 0))
            if price <= 0:
                return Response({
                    'error': 'Price must be greater than 0'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({
                    'message': 'Thali created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except ValueError:
            return Response({
                'error': 'Invalid price format'
            }, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if user owns this thali
        if instance.user != request.user:
            return Response({
                'error': 'You do not have permission to modify this thali'
            }, status=status.HTTP_403_FORBIDDEN)

        # Validate price if provided
        if 'price' in request.data:
            try:
                price = float(request.data['price'])
                if price <= 0:
                    return Response({
                        'error': 'Price must be greater than 0'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    'error': 'Invalid price format'
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Thali updated successfully',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if user owns this thali
        if instance.user != request.user:
            return Response({
                'error': 'You do not have permission to delete this thali'
            }, status=status.HTTP_403_FORBIDDEN)

        # Check if thali is in any active orders
        if instance.cartitem_set.exists():
            return Response({
                'error': 'Cannot delete thali that is in active orders'
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response({
            'message': 'Thali deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    #     representation = super().to_representation(instance)
    #     representation['owner'] = OwnerSerializer(instance.owner).data
    #     return representation
    
    def validate(self, data):
        if Kitchen.objects.filter(owner=data['owner'], name=data['name'], address=data['address']).exists():
            raise serializers.ValidationError("A kitchen with this name and address already exists for this owner.")
        return data
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
    kitchen = KitchenProfileSerializer(read_only=True)
    toppings = ToppingSerializer(many=True, read_only=True)
    topping_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Thali
        fields = ['id', 'kitchen', 'title', 'description', 'price', 
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
