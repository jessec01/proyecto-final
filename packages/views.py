#packages/views.py

#importaciones de rest_framework
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


#importaciones de modelos
from .models import Package

#importaciones de serializers
from .serializer import (PackageSerializer,
                        UpdatePackageSerializer,
                        DetailPackageSerializer,
                        ListPackageSerializer)
# Create your views here.

class PackageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
       return Package.objects.all()
    def get_serializer_class(self):
        #crear
        if self.action == 'create':
            return PackageSerializer
        #editar
        elif self.action in ['update', 'partial_update']:
            return UpdatePackageSerializer
        #detalle
        elif self.action == 'retrieve':
            return DetailPackageSerializer
        #borrar (no necesitas ejecutar destroy aquí, solo retornar un serializer por defecto)
        elif self.action == 'destroy':
            return PackageSerializer
        #lista
        return ListPackageSerializer
