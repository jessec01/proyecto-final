from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from userYC.serializer import UserYCSerializer
from .serializer import YoguiSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from yogui.serializer import YoguiTokenSerializer
#
# Create your views here.
#registro usuario template view
class RegisterUserView(TemplateView):
    template_name = 'yogui/register_user.html'
#lectura del formulario registro usuario
class ReadFormView(APIView):
    serializer_class = UserYCSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_instructor=False, is_yogui=True, is_center_administrator=False)
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#login template view    
class LoginView(TemplateView):
    template_name = 'yogui/login.html'


#el proceso de autenticación se maneja con las vistas de simplejwt en urls.py, no es necesario crear una vista adicional aquí
class YoguiLoginView(TokenObtainPairView):
    serializer_class = YoguiTokenSerializer
# Vista para mostrar el formulario de perfil del yogui
class RegisterProfileView(TemplateView):
    template_name = 'yogui/register_profile.html'
# Vista para procesar el formulario de perfil del yogui
class ReadFormProfileView(APIView):
    serializer_class = YoguiSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                profile = serializer.save()
                return Response(self.serializer_class(profile).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Otras vistas para el dashboard del yogui, visualización de clases, reseñas, etc.
from centeryoga.models import YogaCenter

class YoguiDashboardView(TemplateView):
    template_name = 'yogui/yogui_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers'] = YogaCenter.objects.filter(active=True)
        return context

class YoguiProfileViewSet(viewsets.ModelViewSet):
    serializer_class = YoguiSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        from .models import Yogui
        try:
            return Yogui.objects.filter(user=user)
        except Exception:
            return Yogui.objects.none()

    def perform_create(self, serializer):
        # Asigna el usuario logueado como dueño del perfil de Yogui
        serializer.save(user=self.request.user)
#vista para cerrar sesión del yogui
class LogoutView(APIView):
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
#Vista para mostrar el formulario de reseña de clase 
class ReviewClassView(TemplateView):
    template_name = 'yogui/review_class.html'
#Procesar el formulario de reseña de clase
class ReadReviewClassView(APIView):
    pass