from rest_framework import serializers
from customer.models import Transaction

class RazorpayOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField(max_length=3)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'payment_id', 'order_id', 'signature', 'amount']
        read_only_fields = ['user', 'amount']
    