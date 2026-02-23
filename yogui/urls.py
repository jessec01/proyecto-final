# urls.py (del proyecto principal o de tu app de usuarios)
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterUserView
from .views import ReadFormView, LoginView,  LogoutView, RegisterProfileView,ReadFormProfileView, YoguiDashboardView
from .views import YoguiLoginView
urlpatterns = [
    
    # URL para mostrar el formulario de registro
    path('register/', RegisterUserView.as_view(), name='register'),
    # URL para procesar el formulario de registro
    path('api/register/', ReadFormView.as_view(), name='register_submit'),
    #url para formulario de login
    path('login/',LoginView.as_view(), name='yogui_login'), 
    # URL para obtener el token JWT (login)
    path('api/login/', YoguiLoginView.as_view(), name='token_obtain_pair'), 
    # URL para refrescar el token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #url para mostrar el formulario de registro de perfil del yogui
    path('register/token/profile/', RegisterProfileView.as_view(), name='register_profile'),  
    #url para procesar el formulario de registro de perfil del yogui
    path('api/register-profile/', ReadFormProfileView.as_view(), name='register_profile_submit'),
    #url para cerrar sesión del yogui
    path('logout/', LogoutView.as_view(), name='logout'),
    # Otras URLs para el dashboard del yogui, visualización de clases, reseñas, etc.
    path('dashboard/', YoguiDashboardView.as_view(), name='yogui_dashboard'),
]