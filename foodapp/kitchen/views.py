from django.shortcuts import render
from rest_framework import viewsets ,status
from kitchen.models import * 
from kitchen.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Topping
from .serializers import ToppingSerializer
import os

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

class KitchenProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated ]
    serializer_class = KitchenProfileSerializer
    queryset= KitchenProfile.objects.all()

    
    def create(self, request, *args, **kwargs):
        owner = request.data.get("owner")
        name = request.data.get("name")
        address = request.data.get("address")

        if KitchenProfile.objects.filter(owner=owner, name=name, address=address).exists():
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


class ToppingViewSet(viewsets.ModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if Topping.objects.filter(name__iexact=name).exists():
            return Response({
                'error': 'A topping with this name already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Topping created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        name = request.data.get('name')
        
        # Check for duplicate name only if name is being updated
        if name and name.lower() != instance.name.lower():
            if Topping.objects.filter(name__iexact=name).exists():
                return Response({
                    'error': 'A topping with this name already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Topping updated successfully',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Delete the image file if it exists
        if instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
                
        instance.delete()
        return Response({
            'message': 'Topping deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

class ThaliViewSet(viewsets.ModelViewSet):
    queryset = Thali.objects.all()
    serializer_class = ThaliSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            kitchen = request.user.kitchenprofile
            serializer = self.get_serializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save(kitchen=kitchen)
                return Response({
                    'message': 'Thali created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except ObjectDoesNotExist:
            return Response({
                'error': 'You must have a kitchen profile to create thalis'
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_kitchen = request.user.kitchenprofile
            
            if instance.kitchen != user_kitchen:
                return Response({
                    'error': 'You do not have permission to modify this thali'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # ...rest of your update logic...

        except ObjectDoesNotExist:
            return Response({
                'error': 'You must have a kitchen profile to modify thalis'
            }, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_kitchen = request.user.kitchenprofile
            
            if instance.kitchen != user_kitchen:
                return Response({
                    'error': 'You do not have permission to delete this thali'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # ...rest of your destroy logic...

        except ObjectDoesNotExist:
            return Response({
                'error': 'You must have a kitchen profile to delete thalis'
            }, status=status.HTTP_403_FORBIDDEN)

