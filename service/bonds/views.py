from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from bonds.serializers import BondSerializer
from bonds.models import Bond


class BondsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    
    serializer_class = BondSerializer
    queryset = Bond.objects.filter(buyer_id__isnull=False)    
    
    def buy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {'buyer':request.user}

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)