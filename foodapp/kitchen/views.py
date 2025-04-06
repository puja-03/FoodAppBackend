from django.shortcuts import render
from rest_framework import viewsets
from kitchen.models import *
from kitchen.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class OwnerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OwnerSerializer
    queryset= Owner.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Owner created successfully", "data": response.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Owner updated successfully", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Owner deleted successfully"},
            status=status.HTTP_200_OK
        )

class KitchenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated ]
    serializer_class = KitchenSerializer
    queryset= Kitchen.objects.all()

    
    def create(self, request, *args, **kwargs):
        owner = request.data.get("owner")
        name = request.data.get("name")
        address = request.data.get("address")

        if Kitchen.objects.filter(owner=owner, name=name, address=address).exists():
            return Response(
                {"error": "A kitchen with this name and address already exists for this owner."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Kitchen updated successfully", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Kitchen deleted successfully"},
            status=status.HTTP_200_OK
        )
class BankViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Delete operation is not allowed on Bank details."}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Bank details updated successfully", "data": response.data},
            status=status.HTTP_200_OK
        )
    
class MenuViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get_queryset(self):
        queryset = Menu.objects.all()
        category_id = self.request.query_params.get('category', None)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)  # Filtering by category ID
            
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Category created successfully", "data": response.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Category updated successfully", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_200_OK
        )
    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)  # Case-insensitive search
        return queryset
    


    
        

    


