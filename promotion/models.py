#promotion/models.py
from django.db import models

# Create your models here.
class Promotion(models.Model):
    access_days=models.JSONField()
    access_time=models.JSONField()
    discount_value=models.DecimalField(max_digits=10, decimal_places=2)
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
