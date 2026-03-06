# classsession/models.py
#importaciones de django
from django.db import models
from django.contrib.auth.models import User
#importaciones internas
from yogacenter.models import YogaCenter, ClassYoga

class ClassSession(models.Model):
    """
    Representa una instancia concreta de una clase en un día específico.
    Ej: "Hatha Yoga del Jueves 15 a las 10:00 AM"
    """
    #relacion con classyoga
    class_yoga = models.ForeignKey(ClassYoga, on_delete=models.CASCADE, related_name="sessions")
    #relacion con user
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sessions_taught")
    #relacion con yogacenter
    center = models.ForeignKey(YogaCenter, on_delete=models.CASCADE, related_name="sessions")
    
    #fecha y hora exacta de esta clase
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    #estado para saber si ya pasó o no
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['class_yoga', 'date', 'start_time'] # No puede haber dos clases iguales a la misma hora

    def __str__(self):
        return f"{self.class_yoga.name} - {self.date} {self.start_time}"

    def get_attendees(self):
        """Método helper para obtener los yoguis inscritos en esta sesión específica."""
        return self.attendances.filter(status='PRESENT')

    def get_absentees(self):
        """Método helper para obtener los yoguis ausentes."""
        return self.attendances.filter(status='ABSENT')

    def get_pending(self):
        """Método helper para obtener los yoguis que aún no han sido marcados."""
        return self.attendances.filter(status='PENDING')

    def get_capacity(self):
        """Devuelve la capacidad máxima de la clase."""
        return self.class_yoga.capacity

    def get_booked_count(self):
        """Devuelve cuántos yoguis están inscritos (presentes o pendientes)."""
        return self.attendances.filter(status__in=['PRESENT', 'PENDING']).count()

    def has_space(self):
        """Verifica si quedan cupos disponibles."""
        return self.get_booked_count() < self.get_capacity()

    def get_remaining_capacity(self):
        """Devuelve cuántos cupos quedan."""
        return self.get_capacity() - self.get_booked_count()
