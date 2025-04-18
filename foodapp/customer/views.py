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
        
class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        thali_id = request.data.get('thali')
        quantity = int(request.data.get('quantity', 1))

        existing_item = CartItem.objects.filter(user=user, thali_id=thali_id).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            serializer = CartItemSerializer(existing_item)
            return Response({
                'message': 'Cart item quantity updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({
                    'message': 'Cart item created successfully.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'message': 'Invalid data.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Cart item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({
                "error": "Your cart is empty"
            }, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.get_total_price() for item in cart_items)
        data = request.data.copy()
        data['total_amount'] = total_price
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    thali=cart_item.thali,
                    quantity=cart_item.quantity,
                    price=cart_item.thali.price
                )
                cart_items.delete()
            
            return Response({
                "message": "Order placed successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Order updated successfully", "data": response.data},
            status=status.HTTP_200_OK
        )

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
    
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

