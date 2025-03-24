from .models import *
from rest_framework import serializers
from userapp.auth_serializer import *

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'address', 'city','state','pincode','profile_image', 'created_at']

    def validate_user(self, value):
        if value.role != 'customer':
            raise serializers.ValidationError("User is not a customer")
        return value

        
