#promotion/models.py
from django.db import models
from centeryoga.models import YogaCenter
# Create your models here.
class Promotion(models.Model):
    center = models.ForeignKey(YogaCenter, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    access_days=models.JSONField(null=True, blank=True)
    access_time=models.JSONField(null=True, blank=True)
    discount_value=models.DecimalField(max_digits=10, decimal_places=2)
    discount_type=models.CharField(max_length=50, default='porcentaje')
    active=models.BooleanField(default=True)
    description=models.TextField(null=True, blank=True)
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
