#classyoga/views.py
#importaciones de rest_framework
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

#importaciones de modelos
from .models import YogaCenter

#importaciones de serializers
from .serializer import YogaCenterSerializer,UpdateCenterSerializer,DetailCenterSerializer,ListCenterSerializer

class CenterYogaDashboardView(TemplateView):
    template_name = 'center_administration/center_admin_dashboard.html'
# Create your views here.
class CenterYogaDashboardView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
       return YogaCenter.objects.all()
    def get_serializer_class(self):
        #crear
        if self.action == 'create':
            return YogaCenterSerializer
        #editar
        elif self.action in ['update', 'partial_update']:
            return UpdateCenterSerializer
        #detalle
        elif self.action == 'retrieve':
            return DetailCenterSerializer
        #borrar (no necesitas ejecutar destroy aquí, solo retornar un serializer por defecto)
        elif self.action == 'destroy':
            return YogaCenterSerializer
        #lista
        return ListCenterSerializer
    # En tu ViewSet
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()    
        # --- Tu lógica personalizada aquí ---
        print(f"send a message to the yogui: {instance.name}")
        # ------------------------------------
        # Llamamos al borrado real de la base de datos
        self.perform_destroy(instance)
        return Response(
            {"message": "Center deleted and yoguis notified"}, 
            status=status.HTTP_200_OK # Cambiamos a 200 para enviar el mensaje
        )