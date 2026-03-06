#attendace/views.py
#importaciones de rest_framework
from rest_framework import viewsets
#importaciones internas
from .models import Attendance
from .serializer import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Attendance.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
