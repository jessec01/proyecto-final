from django.views.generic import TemplateView
from rest_framework.views import APIView
from userYC.serializer import UserYCSerializer
from center_administration.serializer import CenterAdministratorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from center_administration.models import CenterAdministrator
from rest_framework.decorators import action
from centeryoga.serializer import MasterSerializer
from django.db import  IntegrityError
from django.db.transaction import TransactionManagementError
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from center_administration.serializer import CenterAdminTokenSerializer
# Create your views here.
#registro usuario template view
class RegisterUserView(TemplateView):
    template_name = 'center_administration/register_user.html'
#lectura del formulario registro usuario
class ReadFormView(APIView):
    serializer_class = UserYCSerializer
    serializer_center = CenterAdministratorSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_instructor=False,is_yogui=False,is_center_administrator=True)
            serializer_center = self.serializer_center(data=request.data)
            if serializer_center.is_valid():
                serializer_center.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#login template view    
class LoginView(TemplateView):
    template_name = 'center_administration/login.html'
#el proceso de autenticación se maneja con las vistas de simplejwt en urls.py, no es necesario crear una vista adicional aquí
class CenterAdminLoginView(TokenObtainPairView):
    serializer_class = CenterAdminTokenSerializer   
# Vista para mostrar el formulario de perfil del center administrator
class RegisterProfileView(TemplateView):
    template_name = 'center_administration/register_profile.html'
# Vista para procesar el formulario de perfil del center administrator

# Otras vistas para el dashboard del center administrator, gestión de centros, etc.
class CenterAdminDashboardView(TemplateView):
    template_name = 'center_administration/center_admin_dashboard.html'
#vista para cerrar sesión del yogui
class LogoutView(APIView):
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
#vista para mostrar el menu de configuracion inicial del center administrator
class DasboardInitialConfigView(TemplateView):
    template_name = 'center_administration/dashboard_initial_config.html'
class ReadDashboardInitialConfigView(viewsets.ModelViewSet):
    queryset = CenterAdministrator.objects.all()
    serializer_class = CenterAdministratorSerializer  # Este es el serializer "normal" para CRUD básico

    # @action(detail=False) significa que NO necesitas poner un ID en la URL
    # La URL será: /api/ttt/procesar_cadena/ (o el nombre que le des)
    @action(detail=False, methods=['post'], url_path='procesar-cadena')
    def procesar_cadena(self, request):
        
        # 1. Instanciar el Maestro con el JSON que llega
        serializer = MasterSerializer(data=request.data)

        # 2. Validar (DRF revisa tipos de datos, campos requeridos, etc.)
        # Si algo falla aquí, DRF devuelve error 400 automáticamente y se detiene.
        try: 
            if serializer.is_valid():
                # 3. Llamar al método create del MasterSerializer
                yogacenter = serializer.save(user=request.user)  # Aquí se ejecuta tu lógica personalizada de creación
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'error': 'Integrity error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        except TransactionManagementError as e:
            return Response({'error': 'Transaction error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        # 4. Responder al Frontend
        # Como tu create devuelve el objeto 'nuevo_fff', podemos serializarlo
        # para devolver los datos creados, o simplemente mandar un mensaje de éxito.
        
        return Response({
            'mensaje': 'Proceso completado exitosamente'
        }, status=status.HTTP_201_CREATED)