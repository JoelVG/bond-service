from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bonds.models import Bond
from bonds.serializers import BondSerializer

class BondsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    
    serializer_class = BondSerializer
    queryset = Bond.objects.filter(buyer_id__isnull=True)    
    permission_classes = [IsAuthenticated]
    
    def buy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {'buyer':request.user.id}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

        
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('currency') == 'USD':
            return Bond.objects.get_usd(queryset)
        return queryset