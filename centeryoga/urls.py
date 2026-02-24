#centeryoga/urls.py
#importaciones de librerias django
from django.urls import path
#libreria externa
from rest_framework.routers import DefaultRouter
#libreria interna
from .views import (
    CenterYogaDashboardView,DashboardCenterView,HomeView    
)
router = DefaultRouter()
router.register(r'centers', CenterYogaDashboardView, basename='center-yoga-dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardCenterView.as_view(), name='dashboard-center'),
    path('home/', HomeView.as_view(), name='home'),
]