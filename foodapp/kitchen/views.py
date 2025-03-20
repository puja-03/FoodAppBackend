from django.shortcuts import render
from rest_framework import viewsets
from kitchen.models import *
from kitchen.serializers import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class OwnerViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    queryset= Owner.objects.all()

class KitchenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated ]
    serializer_class = KitchenSerializer
    queryset= Kitchen.objects.all()

class BankViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

