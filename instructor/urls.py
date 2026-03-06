from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic import TemplateView
from .views import RegisterUserView
from .views import ReadFormView, LoginView  
from instructor.views import RegisterProfileView, ReadProfileView, InstructorDashboardView, LogoutView
urlpatterns = [
    # URL para mostrar el formulario de registro
    path('register/', RegisterUserView.as_view(), name='instructor_register'),
    # URL para procesar el formulario de registro
    path('api/register/', ReadFormView.as_view(), name='instructor_register_submit'),
    # URL para mostrar el formulario de login
    path('login/',LoginView.as_view(), name='instructor_login'),
    # URL para obtener el token JWT (login)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Este es el Login
    # URL para refrescar el token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #url para mostrar el formulario de registro de perfil del yogui
    path('register/token/profile/', RegisterProfileView.as_view(), name='register_profile'),
    #url para procesar el formulario de registro de perfil del yogui
    path('api/register-profile/', ReadProfileView.as_view(), name='register_profile_submit'),
    #url para cerrar sesión del instructor
    path('logout/', LogoutView.as_view(), name='logout'),
    # Otras URLs para el dashboard del instructor, gestión de clases, etc.
    path('api/dashboard/', InstructorDashboardView.as_view({'get': 'list', 'post': 'create'}), name='instructor_dashboard_api'),
    path('api/dashboard/<int:pk>/', InstructorDashboardView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='instructor_dashboard_detail'),
    path('dashboard/', TemplateView.as_view(template_name='instructor/instructor_dashboard.html'), name='instructor_dashboard'),
]