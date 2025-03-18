from django.shortcuts import render
from rest_framework import viewsets
from kitchen.models import *
from kitchen.serializers import *

# Create your views here.
class OwnerViewSet(viewsets.ModelViewSet):
    queryset= Owner.objects.all()
    serializer_class = OwnerSerializer
