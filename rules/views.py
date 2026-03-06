#rules/views.py

#importaciones de rest_framework
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

#importaciones de modelos
from .models import Rule

#importaciones de serializers
from .serializer import(
    RuleSerializer,
    UpdateRuleSerializer,
    DetailRuleSerializer,
    ListRuleSerializer
)
# Create your views here.

class RuleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
       return Rule.objects.all()
    def get_serializer_class(self):
        #crear
        if self.action == 'create':
            return RuleSerializer
        #editar
        elif self.action in ['update', 'partial_update']:
            return UpdateRuleSerializer
        #detalle
        elif self.action == 'retrieve':
            return DetailRuleSerializer
        #borrar (no necesitas ejecutar destroy aquí, solo retornar un serializer por defecto)
        elif self.action == 'destroy':
            return RuleSerializer
        #lista
        return ListRuleSerializer
