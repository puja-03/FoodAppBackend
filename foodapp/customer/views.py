from django.shortcuts import render
from .models import *
from rest_framework import viewsets
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from userapp.permissions import IsCustomer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsCustomer]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        customer = Customer.objects.filter(user=user)
        if customer.exists():
            return Response({"error": "Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({
                "message": "Customer Profile Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)
    
    
    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()

        name = data.get("name")
        phone_number = data.get("phone_number")

        if name:
            user.name = name
        if phone_number:
            user.phone_number = phone_number
        user.save()

        # Update profile fields
        customer_profile = Customer.objects.filter(user=user).first()
        if customer_profile:
            serializer = self.get_serializer(customer_profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                # Fetch updated user data
                user_data = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "is_verified": user.is_verified
                }

                profile_data = serializer.data
                profile_data["user"] = user_data  

                return Response(
                    {
                        "detail": "Profile updated successfully.",
                        "profile": profile_data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            customer_profile = Customer.objects.get(user=user)
            customer_profile.delete()
            return Response({"detail": "Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)