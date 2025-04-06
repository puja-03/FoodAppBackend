from rest_framework import serializers
from kitchen.models import *



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


class KitchenSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all()) 
    class Meta:
        model = Kitchen
        fields = "__all__"

    # def to_representation(self, instance):
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


