#promotion/views.py

#importaciones de rest_framework
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

#importaciones de modelos
from .models import Promotion

#importaciones de serializers
from .serializer import (
    PromotionSerializer,
    UpdatePromotionSerializer,
    DetailPromotionSerializer,
    ListPromotionSerializer
)
# Create your views here.

class PromotionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
       return Promotion.objects.all()
    def get_serializer_class(self):
        #crear
        if self.action == 'create':
            return PromotionSerializer
        #editar
        elif self.action in ['update', 'partial_update']:
            return UpdatePromotionSerializer
        #detalle
        elif self.action == 'retrieve':
            return DetailPromotionSerializer
        #borrar (no necesitas ejecutar destroy aquí, solo retornar un serializer por defecto)
        elif self.action == 'destroy':
            return PromotionSerializer
        #lista
        return ListPromotionSerializer
