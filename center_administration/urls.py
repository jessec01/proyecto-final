from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from center_administration.views import CenterAdminDashboardView, DasboardInitialConfigView, LogoutView, ReadDashboardInitialConfigView

from .views import RegisterUserView, ReadFormView, LoginView

urlpatterns = [
    #registro usuario
    #template view
    #url para mostrar el formulario de registro de usuario
    path('register/', RegisterUserView.as_view(),
     name='register'),
    #url para procesar el formulario de registro de usuario
    path('api/register/', ReadFormView.as_view(),
     name='read_form'),    
    #inicio de sesión    #url para mostrar el formulario de login
    path('login/', LoginView.as_view(), name='login'),
    #Authentication con JWT
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #refrescar token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #registro perfil template view
    
   #url para mostrar el dashboard del center administrator
    path('dashboard/config/', DasboardInitialConfigView.as_view(), name='center_admin_dashboard'),
    #url para mostrar el formulario de registro de perfil del center administrator,del centro de yoga
    #reglas centro, tipos de reglas de paquetes, reglas de pagos, etc.
    path('api/dashboard/config/initial/', ReadDashboardInitialConfigView.as_view(), name='dashboard_initial_config'),

    #url para cerrar sesión del center administrator
    path('logout/', LogoutView.as_view(), name='logout'),
    # Otras URLs para el dashboard del center administrator, gestión de centros, etc.
    path('dashboard/config/', DashboardInitialConfigView.as_view(), name='dashboard_initial_config'),

    #read form dashboard template view
   
    #cerrar sesión template view
    


]
