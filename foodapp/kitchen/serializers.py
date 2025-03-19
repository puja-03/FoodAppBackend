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
