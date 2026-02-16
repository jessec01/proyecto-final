from django.views.generic import TemplateView
from rest_framework import viewsets
from centeryoga.models import YogaCenter    
from .serializer import ProductoSerializer
#esta el vista de la pagina principal del centro
class HomeView(TemplateView):
    template_name = "homeview.html"
#vista para crear un nuevo centro de yoga
class dasboardCenterView(TemplateView):
    template_name = "dashboard_center.html"
# views.py
#CRUD update, delete, read, create YogaCenter
class CenterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YogaCenter.objects.all()
    serializer_class = ProductoSerializer