from django.shortcuts import render
from rest_framework import viewsets
from Delivery_panel.models import *
from Delivery_panel.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class Delivery_boyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = Delivery_boySerializer
    queryset= Delivery_boy.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Delivery_boy created successfully", "data": response.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Delivery_boy updated successfully", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Delivery_boy deleted successfully"},
            status=status.HTTP_200_OK
        )

