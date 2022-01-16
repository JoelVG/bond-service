from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bonds.models import Bond


class BondSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bond
        fields = ('buyer', 'seller', 'name', 'quantity', 'price')