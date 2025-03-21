from django.shortcuts import render
from django.http import HttpResponse
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


# Create your views here.
class AdminView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        return HttpResponse("this is Admin Panel")

class OwnerView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def get(self, request):
        return HttpResponse("this is Owner Panel")
    
class CustomerView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    def get(self, request):
        return HttpResponse("this is User Panel")
    
class DeliveryBoyView(APIView):
    permission_classes = [IsAuthenticated, IsDeliveryBoy]
    def get(self, request):
        return HttpResponse("this is Delivery Panel")