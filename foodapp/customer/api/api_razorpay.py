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

       
# class RazorpayClient:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(RazorpayClient, cls).__new__(cls)
#             cls._instance.client = razorpay.Client(
#                 auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
#         return cls._instance

#     def create_order(self, amount, currency="INR"):
#         try:
#             data = {
#                 "amount": amount * 100,
#                 "currency": currency
#             }
#             return self.client.order.create(data=data)
#         except Exception as e:
#             raise ValidationError({
#                 "status_code": 400,
#                 "message": f"Order creation failed: {str(e)}"
#             })

#     def verify_payment(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
#         try:
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': razorpay_payment_id,
#                 'razorpay_signature': razorpay_signature
#             }
#             return self.client.utility.verify_payment_signature(params_dict)
#         except Exception as e:
#             raise ValidationError({
#                 "status_code": 400,
#                 "message": f"Payment verification failed: {str(e)}"
#             })
class RazorpayClient:
    def __init__(self):
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

    def verify_payment(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            # Generate the expected signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            # Log verification attempt
            print(f"Verifying payment with params: {params_dict}")
            
            # Verify signature
            is_valid = self.client.utility.verify_payment_signature(params_dict)
            
            if not is_valid:
                raise ValidationError({
                    "status_code": 400,
                    "message": "Invalid payment signature"
                })
                
            return True

        except razorpay.errors.SignatureVerificationError as e:
            print(f"Signature verification failed: {str(e)}")
            raise ValidationError({
                "status_code": 400,
                "message": f"Payment signature verification failed: {str(e)}"
            })
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
                # Create an instance of RazorpayClient
                client = RazorpayClient()
                
                # Verify the payment using the instance
                client.verify_payment(
                    razorpay_order_id=request.data.get('razorpay_order_id'),
                    razorpay_payment_id=request.data.get('razorpay_payment_id'),
                    razorpay_signature=request.data.get('razorpay_signature')
                )

                # Create transaction
                transaction = Transaction.objects.create(
                    user=request.user,
                    payment_id=request.data.get('razorpay_payment_id'),
                    order_id=request.data.get('razorpay_order_id'),
                    signature=request.data.get('razorpay_signature'),
                    amount=request.data.get('amount')
                )

                return Response({
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Transaction created successfully",
                    "data": TransactionSerializer(transaction).data
                }, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class TransactionAPIView(APIView):
#     def post(self, request):
#         serializer = TransactionSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             payment_id = request.data.get('razorpay_payment_id')
#             order_id = request.data.get('razorpay_order_id')
#             signature = request.data.get('razorpay_signature')
#             amount = request.data.get('amount')

#             try:
#                 rz_client.verify_payment(
#                     razorpay_order_id=order_id,
#                     razorpay_payment_id=payment_id,
#                     razorpay_signature=signature
#                 )
#             except ValidationError as e:
#                 return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

#             # Create a transaction record
#             transaction = Transaction.objects.create(
#                 user=user,
#                 payment_id=payment_id,
#                 order_id=order_id,
#                 signature=signature,
#                 amount=amount
#             )
#             response = {
#                 "status_code": status.HTTP_200_OK,
#                 "message": "Transaction created successfully",
#                 "data": TransactionSerializer(transaction).data
#             }
#             return Response(response, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        