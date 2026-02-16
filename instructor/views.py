from django.views.generic import TemplateView
from rest_framework.views import APIView
from userYC.serializer import UserYCSerializer
from .serializer import InstructorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

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
            serializer.save(is_instructor=True, is_yogui=False, is_center_administrator=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
    authentication_classes = [TokenAuthentication]
    
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
class InstructorDashboardView(TemplateView):
    template_name = 'instructor/instructor_dashboard.html'
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