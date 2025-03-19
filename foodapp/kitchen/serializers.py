from rest_framework import serializers
from kitchen.models import *

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"
