#attendace/models.py
#importaciones de django
from django.db import models
#importaciones internas
from classsession.models import ClassSession
from yogui.models import Yogui

class Attendance(models.Model):
    """
    Registra la asistencia de un Yogui a una sesión específica.
    """
    #relacion con classsession
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="attendances")
    #relacion con yogui
    yogui = models.ForeignKey(Yogui, on_delete=models.CASCADE, related_name="attendances")
    
    #estado de la asistencia
    STATUS_CHOICES = [
        ('PRESENT', 'Presente'),
        ('ABSENT', 'Ausente'),
        ('PENDING', 'Pendiente'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    #fecha y hora del registro
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
        unique_together = ['session', 'yogui'] # Un yogui solo puede tener un registro por sesión

    def __str__(self):
        return f"{self.yogui.user.username} - {self.session.class_yoga.name} - {self.status}"
