from rest_framework import serializers
from kitchen.models import *

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"

class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = "__all__"

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"
