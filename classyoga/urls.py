from django.urls import path
from .views import CenterYogaDashboardView

urlpatterns = [
    path('dashboard/config/', CenterYogaDashboardView.as_view(), name='dashboard_main'),
    path('dashboard/', CenterYogaDashboardView.as_view(), name='dashboard_main'),
]