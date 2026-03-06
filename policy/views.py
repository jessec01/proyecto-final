#policy/views.py

#importaciones de rest_framework
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

#importaciones de modelos
from .models import Policy

#importaciones de serializers
from .serializer import (
    PolicySerializer,
    UpdatePolicySerializer,
    DetailPolicySerializer,
    ListPolicySerializer
)

class PolicyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
       return Policy.objects.all()
    def get_serializer_class(self):
        #crear
        if self.action == 'create':
            return PolicySerializer
        #editar
        elif self.action in ['update', 'partial_update']:
            return UpdatePolicySerializer
        #detalle
        elif self.action == 'retrieve':
            return DetailPolicySerializer
        #borrar (no necesitas ejecutar destroy aquí, solo retornar un serializer por defecto)
        elif self.action == 'destroy':
            return PolicySerializer
        #lista
        return ListPolicySerializer
