from django.shortcuts import render
from .models import *
from rest_framework import viewsets, status
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
        

class ThaliViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ThaliSerializer
    queryset = Thali.objects.all()

    def get_permissions(self):
        """
        Only admin users can create, update or delete thalis
        Regular users can only view them
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Thali.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(toppings__name=category)
        return queryset

    def update(self, request, *args, **kwargs):
        thali = self.get_object()
        data = request.data.copy()
        
        # Validate price changes
        if 'price' in data and float(data['price']) <= 0:
            return Response(
                {"error": "Price must be greater than zero"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(thali, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Thali updated successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        thali = self.get_object()
        
        # Check if thali is in any active orders
        active_orders = thali.cartitem_set.filter(
            order__order_status__in=['PENDING', 'CONFIRMED', 'PREPARING']
        ).exists()
        
        if active_orders:
            return Response({
                "error": "Cannot delete thali with active orders"
            }, status=status.HTTP_400_BAD_REQUEST)

        thali.delete()
        return Response({
            "message": "Thali deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)

class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.user != request.user:
            return Response(
                {"error": "Not authorized to update this cart item"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.user != request.user:
            return Response(
                {"error": "Not authorized to delete this cart item"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        cart_item.delete()
        return Response(
            {"message": "Cart item removed successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Order placed successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user:
            return Response(
                {"error": "Not authorized to update this order"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only allow updating certain fields
        allowed_updates = ['delivery_address']
        data = {k: v for k, v in request.data.items() if k in allowed_updates}
        
        serializer = self.get_serializer(order, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user:
            return Response(
                {"error": "Not authorized to cancel this order"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        if order.order_status not in ['PENDING', 'CONFIRMED']:
            return Response(
                {"error": "Cannot cancel order in current status"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        order.order_status = 'CANCELLED'
        order.save()
        return Response(
            {"message": "Order cancelled successfully"}, 
            status=status.HTTP_200_OK
        )