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

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"
