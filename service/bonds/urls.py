from django.urls import path
from bonds.views import BondsViewSet


detail = BondsViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})
buy = BondsViewSet.as_view({'put': 'buy'})
index = BondsViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('bonds', index, name='bonds-list'),
    path('bonds/<str:pk>', detail, name='bonds-detail'),
    path('bonds/<str:pk>/buy', buy, name='bonds-buy')
]