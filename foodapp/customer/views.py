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
            return Response({"error": "Customer Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
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
    
    def patch(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(id=kwargs['pk'])
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Customer Profile Updated Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)