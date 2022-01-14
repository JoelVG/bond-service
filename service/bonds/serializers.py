from rest_framework import serializers
from bonds.models import Bond
from rest_framework.exceptions import ValidationError


class BondSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bond
        fields = ('buyer', 'seller', 'name', 'quantity', 'price')
        
    def validate_buyer(self, value):
        if self.instance is not None and self.instance.buyer_id is not None:
            raise serializers.ValidationError("Bond already bought")
        return value