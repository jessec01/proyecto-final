#instructor/views.py
from django.db import  transaction
from django.views.generic import TemplateView

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework import (viewsets,status)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from userYC.serializer import UserYCSerializer
from instructor.models import Instructor
from .serializer import (InstructorSerializer,
InstructorUpdateSerializer,
DetailInstructorSerializer,LoginSerializer, InstructorListSerializer )
# Create your views here.
#registro usuario template view
class RegisterUserView(TemplateView):
    template_name = 'instructor/register_user.html'
#lectura del formulario registro usuario
class ReadFormView(APIView):
    serializer_class = UserYCSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        try: 
            serializer.is_valid(raise_exception=True)
            user = serializer.save(is_instructor=True, is_yogui=False, is_center_administrator=False)
            return Response({"id": user.id, "user": {"id": user.id}}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except transaction.TransactionManagementError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#login template view 
class LoginView(TemplateView):
    template_name = 'instructor/login.html'
#la vista de authentication se maneja con las vistas de simplejwt en urls.py, no es necesario crear una vista adicional aquí

# Vista para mostrar el formulario de perfil del instructor
class RegisterProfileView(TemplateView):
    template_name = 'instructor/register_profile.html'

# Vista para procesar el formulario de perfil del instructor
class ReadProfileView(APIView):
    
    serializer_class =InstructorSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user=request.user
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except transaction.TransactionManagementError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Otras vistas para el dashboard del instructor, gestión de clases, etc.        
class InstructorDashboardView(viewsets.ModelViewSet):
    serializer_class = InstructorSerializer  # No olvides definir el serializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # 1. Obtenemos el usuario autenticado que está haciendo la solicitud
        user = self.request.user
        # 2. Navegamos desde la tabla base (User) hasta el perfil CenterAdministrator
        # y de allí sacamos el campo yoga_center
        # La forma correcta según tus modelos es user.centeradministrator.yoga_center
        admin_center = user.centeradministrator.yoga_center
        return Instructor.objects.filter(yogacenter=admin_center)
    def get_serializer_class(self):
        #crear
        if self.action == 'create':
            return InstructorSerializer
        #editar
        elif self.action in ['update', 'partial_update']:
            return InstructorUpdateSerializer
        #detalle
        elif self.action == 'retrieve':
            return DetailInstructorSerializer
        #lista
        return InstructorListSerializer
#vista para cerrar sesión del instructor    
class LogoutView(TemplateView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Recibimos el token de refresco del cliente
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            
            # Lo mandamos a la lista negra (Blacklist)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)