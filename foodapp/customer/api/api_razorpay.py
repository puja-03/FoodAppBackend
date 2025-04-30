from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .razorpay_serilizers import RazorpayOrderSerializer,TransactionSerializer
from customer.api.razorpay.main import RazorpayClient
from rest_framework.serializers import ValidationError
from customer.models import Transaction



rz_client = RazorpayClient()
class RazorpayOrderView(APIView):
    def post(self, request):
        serializer = RazorpayOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = rz_client.create_order(
                amount=serializer.validated_data.get("amount"),
                currency=serializer.validated_data.get("currency")
            )
            response ={
                "status_code": status.HTTP_200_OK,
                "message": "Order created successfully",
                "data": order
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
def verify_payment(self , razorpay_order_id, razorpay_payment_id, razorpay_signature):
    try:
        return client.utityy.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except Exception as e:
        raise ValidationError({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": str(e),
        })
   

class TransactionAPIView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            payment_id = request.data.get('razorpay_payment_id')
            order_id = request.data.get('razorpay_order_id')
            signature = request.data.get('razorpay_signature')
            amount = request.data.get('amount')

            try:
                rz_client.verify_payment(
                    razorpay_order_id=order_id,
                    razorpay_payment_id=payment_id,
                    razorpay_signature=signature
                )
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

            # Create a transaction record
            transaction = Transaction.objects.create(
                user=user,
                payment_id=payment_id,
                order_id=order_id,
                signature=signature,
                amount=amount
            )
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "Transaction created successfully",
                "data": TransactionSerializer(transaction).data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)