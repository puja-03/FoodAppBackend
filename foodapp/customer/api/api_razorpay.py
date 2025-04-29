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
        
