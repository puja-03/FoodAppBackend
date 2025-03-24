from .models import *
from rest_framework import serializers
import random

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'role', 'is_active', 'is_verified','phone_number', 'password']
        extra_kwargs = {
            "password": {'write_only': True},
            "email": {'required': True},
            "name": {'required': True},
            }

    def create(self, validated_data): 
        email = validated_data['email']
        name = validated_data['name']
        role = validated_data.get('role', 'customer') 

        base_username = email.split('@')[0]
        username = base_username
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{random.randint(1000, 9999)}"
        user = CustomUser(
            email=email,
            name=name,
            username=username,
            role=role
        )
        if user.role == 'admin':
            user.is_staff = True
        user.set_password(validated_data['password']) 
        user.save()
        return user
        
# otp verify email serializer
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()