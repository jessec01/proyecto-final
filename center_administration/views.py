#centro_administracion/views.py
#importaciones propia de python

#importaciones de django
from django.db import models, IntegrityError, transaction
from django.views.generic import TemplateView
#importaciones de rest_framework
from rest_framework import status
from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView

#importaciones propia de la app
from center_administration.serializer import (
    CenterAdminSerializer,
    CenterAdminTokenSerializer,
    CenterAdministratorSerializer,
    CenterAdminConfiginitialSerializer
)
from center_administration.models import CenterAdministrator
from invoice.models import Invoice
from userYC.serializer import UserYCSerializer
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

#Vista desactivada hasta que se pase los test de los demas modelos
class ReadDashboardInitialConfigView(viewsets.ModelViewSet):
    queryset = CenterAdministrator.objects.all()
    serializer_class = CenterAdministratorSerializer  # Este es el serializer "normal" para CRUD básico
    permission_classes = [IsAuthenticated]

    # @action(detail=False) significa que NO necesitas poner un ID en la URL
    # La URL será: /api/ttt/procesar_cadena/ (o el nombre que le des)
    @action(detail=False, methods=['post'], url_path='procesar-cadena')
    def procesar_cadena(self, request):
        # 1. Instanciar el Maestro con el JSON que llega
        serializer = CenterAdminConfiginitialSerializer(data=request.data)

        # 2. Validar (DRF revisa tipos de datos, campos requeridos, etc.)
        # Si algo falla aquí, DRF devuelve error 400 automáticamente y se detiene.
        try: 
            if serializer.is_valid(raise_exception=True):
                # 3. Llamar al método create del MasterSerializer
                yoga_center = serializer.save(user=request.user)  # Aquí se ejecuta tu lógica personalizada de creación
                print("Centro de Yoga creado:", yoga_center)  # Solo para debug, puedes eliminarlo después
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'error': 'Integrity error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        except transaction.TransactionManagementError as e:
            return Response({'error': 'Transaction error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        # 4. Responder al Frontend
        # Como tu create devuelve el objeto 'nuevo_fff', podemos serializarlo
        # para devolver los datos creados, o simplemente mandar un mensaje de éxito.
        
        return Response({
            'mensaje': 'Proceso completado exitosamente'
        }, status=status.HTTP_201_CREATED)
class CenterAdminProfileView(TemplateView):
    template_name = 'center_administration/center_admin_profile.html'
# Otras vistas para el dashboard del instructor, gestión de clases, etc.        
class CenterAdminControlProfileView(viewsets.ModelViewSet):
    serializer_class = CenterAdminSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # 1. Obtenemos el usuario autenticado que está haciendo la solicitud
        user = self.request.user
        # 2. Navegamos desde la tabla base (User) hasta el perfil CenterAdministrator
        try:
            admin_center = user.centeradministrator.yoga_center
            return CenterAdministrator.objects.filter(yoga_center=admin_center)
        except Exception:
            # Si el usuario no ha hecho la mega-transacción, "centeradministrator" no existe ni en DB
            return CenterAdministrator.objects.none()
    def get_serializer_class(self):
        return CenterAdminSerializer

class CenterAdminCenterEditView(TemplateView):
    template_name = 'center_administration/center_admin_center_edit.html'

class CenterAdminPackagesView(TemplateView):
    template_name = 'center_administration/center_admin_packages.html'

class CenterAdminPromotionsView(TemplateView):
    template_name = 'center_administration/center_admin_promotions.html'


class CenterAdminInvoicesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Encontrar el centro de yoga logueado
            admin_center = request.user.centeradministrator.yoga_center
            
            # Limpiar: Si hay facturas nulas (sin pdf) de este centro, se eliminan
            Invoice.objects.filter(pay__package__yoga_center=admin_center).filter(
                models.Q(invoice_file__isnull=True) | models.Q(invoice_file='')
            ).delete()
            
            # Obtener facturas buenas
            invoices = Invoice.objects.filter(pay__package__yoga_center=admin_center, active=True).order_by('-issued_at')
            
            data = []
            for inv in invoices:
                # Nos protegemos en caso de que paquete ya no exista
                pkg_name = inv.pay.package.name if (inv.pay and inv.pay.package) else "Paquete General"
                
                data.append({
                    'id': inv.id,
                    'invoice_number': inv.invoice_number,
                    'client_name': inv.client_name,
                    'client_document': inv.client_document,
                    'total_amount': str(inv.total_amount),
                    'issued_at': inv.issued_at.strftime('%Y-%m-%d %H:%M'),
                    'file_url': inv.invoice_file.url if inv.invoice_file else None,
                    'package_name': pkg_name
                })
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)