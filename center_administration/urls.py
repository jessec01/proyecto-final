#center_administration/urls.py
#importaciones de django
from django.urls import path, include

#importaciones de rest_framework
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework import routers
#importaciones de center_administration
from .views import (
    CenterAdminControlProfileView,
    CenterAdminDashboardView,
    CenterAdminLoginView,
    CenterAdminProfileView,
    LoginView,
    LogoutView,
    RegisterUserView,
    ReadFormView,
    DasboardInitialConfigView,
    ReadDashboardInitialConfigView,
    CenterAdminControlProfileView,
    CenterAdminCenterEditView,
    CenterAdminPackagesView,
    CenterAdminPromotionsView,
    CenterAdminInvoicesView
)
router = routers.DefaultRouter()
router.register(r'center_administrator', CenterAdminControlProfileView, basename='center_administrator')
urlpatterns = [
    #registro usuario
    #template view
    #url para mostrar el formulario de registro de usuario
    path('register/', RegisterUserView.as_view(),
     name='center_admin_register'),
    #url para procesar el formulario de registro de usuario
    path('api/register/', ReadFormView.as_view(),
     name='read_form'),    
    #inicio de sesión    #url para mostrar el formulario de login
    path('login/', LoginView.as_view(), name='center_admin_login'),
    #Authentication con JWT
    path('api/login/', CenterAdminLoginView.as_view(), name='token_obtain_pair'),
    #refrescar toke
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #registro perfil template view
    path('profile/', CenterAdminProfileView.as_view(), name='center_admin_profile'),
   #controla el CRUD 
   path('api/', include(router.urls)),
   #url para mostrar el dashboard del center administrator
    path('dashboard/', CenterAdminDashboardView.as_view(), name='dashboard_main'),
    path('dashboard/config/', DasboardInitialConfigView.as_view(), name='center_admin_dashboard'),
    #url para mostrar el formulario de registro de perfil del center administrator,del centro de yoga
    #reglas centro, tipos de reglas de paquetes, reglas de pagos, etc.
    path('api/dashboard/config/', ReadDashboardInitialConfigView.as_view({'post': 'procesar_cadena'}), name='dashboard_initial_config'),
    
    # Hace falta crear las vista de los dsboard secundarios
    # y el panel central de administracion de centros
    path('center_edit/', CenterAdminCenterEditView.as_view(), name='center_admin_center_edit'),
    path('packages/', CenterAdminPackagesView.as_view(), name='center_admin_packages'),
    path('promotions/', CenterAdminPromotionsView.as_view(), name='center_admin_promotions'),
    path('api/invoices/', CenterAdminInvoicesView.as_view(), name='center_admin_invoices'),

    #url para cerrar sesión del center administrator
    path('logout/', LogoutView.as_view(), name='logout'),
    # Otras URLs para el dashboard del center administrator, gestión de centros, etc.

    #read form dashboard template view
   
    #cerrar sesión template view
    


]
