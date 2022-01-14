from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from bonds.models import Bond
from bonds.serializers import BondSerializer


class BondsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    
    serializer_class = BondSerializer
    queryset = Bond.objects.filter(buyer_id__isnull=True)    
    
    def buy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {'buyer':request.user}

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    
    def list_bonds_to_sell(self, request, *args, **kwargs):
        instance = self.get_object()
        