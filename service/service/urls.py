from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def service_check(request):
    return Response({'message':'ok'})


urlpatterns = [
    path('service-check/', service_check),
    path('api/', include('bonds.urls')),
    path('admin/', admin.site.urls)
]
