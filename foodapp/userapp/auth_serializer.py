from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'role', 'is_active', 'is_verified', 'password']
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):  
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'customer')  
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user