import razorpay
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .razorpay_serilizers import RazorpayOrderSerializer,TransactionSerializer
from customer.api.razorpay.main import RazorpayClient
from rest_framework.serializers import ValidationError
from customer.models import Transaction
import random
import string
import hashlib
from django.conf import settings

def generate_random_string(length=20):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
rz_client = RazorpayClient()
class RazorpayOrderView(APIView):
    def post(self, request):
        serializer = RazorpayOrderSerializer(data=request.data)
        if serializer.is_valid():
            # Generate random payment_id and signature
            random_payment_id = generate_random_string()
            random_signature = hashlib.sha256(generate_random_string().encode()).hexdigest()
            
            order = rz_client.create_order(
                amount=serializer.validated_data.get("amount"),
                currency=serializer.validated_data.get("currency")
            )
            # Add payment_id and signature to order data
            order['payment_id'] = random_payment_id
            order['signature'] = random_signature
            
            response ={
                "status_code": status.HTTP_200_OK,
                "message": "Order created successfully",
                "data": order
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
#     try:
#         return client.utility.verify_payment_signature({
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': razorpay_payment_id,
#             'razorpay_signature': razorpay_signature
#         })
#     except Exception as e:
#         raise ValidationError({
#             "status_code": 400,
#             "message": f"Payment verification failed: {str(e)}"
#         })     

# class TransactionAPIView(APIView):
#     def post(self, request):
#         serializer = TransactionSerializer(data=request.data)
#         if serializer.is_valid():
#             rz_client.verify_payment(   
#                 razorpay_order_id=request.data.get('razorpay_order_id'),
#                 razorpay_payment_id=request.data.get('razorpay_payment_id'),
#                 razorpay_signature=request.data.get('razorpay_signature')
#             )
#             serializer.save(user=request.user)
#             response = {
#                 "status_code": status.HTTP_200_OK,
#                 "message": "Transaction created successfully",
#             }
#             return Response(response, status=status.HTTP_201_CREATED)
#         else:
#             response = {    
#                 "status_code": status.HTTP_400_BAD_REQUEST,
#                 "message": "Transaction creation failed",
#                 "errors": serializer.errors
#             }
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RazorpayClient:
    def __init__(self):
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

    def verify_payment(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """
        Verify Razorpay payment signature
        """
        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            print(f"Verifying payment with order_id: {razorpay_order_id}")
            
            self.client.utility.verify_payment_signature(params_dict)
            
            payment = self.client.payment.fetch(razorpay_payment_id)
            if payment['status'] != 'captured':
                raise ValidationError({
                    "status_code": 400,
                    "message": f"Payment not captured. Status: {payment['status']}"
                })

            return True
        except Exception as e:
            print(f"Payment verification failed: {str(e)}")
            raise ValidationError({
                "status_code": 400,
                "message": f"Payment verification failed: {str(e)}"
            })

class TransactionAPIView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                rz_client = RazorpayClient()
                
                rz_client.verify_payment(
                    razorpay_order_id=request.data.get('razorpay_order_id'),
                    razorpay_payment_id=request.data.get('razorpay_payment_id'),
                    razorpay_signature=request.data.get('razorpay_signature')
                )

                # Create trnsaction after verification
                transaction = serializer.save(user=request.user)
                
                return Response({
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Transaction completed successfully",
                    "data": TransactionSerializer(transaction).data
                }, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)