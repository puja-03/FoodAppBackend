from .models import *
from rest_framework import serializers
from userapp.auth_serializer import *

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
        
        
