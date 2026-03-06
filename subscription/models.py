#subscription/models.py

#Importaciones django   
from django.db import models

#Importaciones internas
from yogui.models import Yogui
# Create your models here.
class Subscription(models.Model):
    yogui=models.ForeignKey(Yogui, on_delete=models.CASCADE)
    date_start=models.DateField()
    date_end=models.DateField()
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.yogui} - {self.date_start} - {self.date_end}'