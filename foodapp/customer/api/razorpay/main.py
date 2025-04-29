from .import client
from rest_framework.serializers import ValidationError
from rest_framework import status
class RazorpayClient:
    def create_order(self, amount, currency):
        # Simulate creating an order with Razorpay
        data = {
            "amount": 100,
            "currency": "INR",
        }
        try:
            order_data = client.order.create(data=data)
            return order_data
        except Exception as e:
            raise ValidationError({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": e,
            }      
            )
