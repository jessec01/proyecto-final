#system_help/models.py
#importaciones de librerias
from django.db import models

#importaciones de modelos
from .models import YogaCenter

# Create your models here.
class SystemHelp(models.Model):
    module_name=models.CharField(unique=True,max_length=100,
    help_text='Ejemplo: Usuarios, Centros de Yoga, Clases, etc.')
    general_description=models.TextField(unique=True,max_length=500,
    help_text='Explica detalladamente para que sirve el modulo')
    is_required=models.BooleanField(default=False,
    help_text='Indica si el modulo es requerido para el funcionamiento del sistema')
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.module_name

class FieldGuide(models.Model):
    module=models.ForeignKey(SystemHelp,on_delete=models.CASCADE,
    help_text='Modulo al que pertenece el campo')
    label_frontend=models.CharField(max_length=100,
    help_text='Nombre del campo en el frontend')
    user_instruction=models.TextField(max_length=500,
    help_text='Instruccion para el usuario. Ejemplo: Ingrese el nombre del centro de yoga')
    example_value=models.CharField(max_length=100,
    help_text='Ejemplo de valor. Ejemplo: Centro de Yoga')

    #reglas y validaciones
    min_length_or_value=models.CharField(max_length=50,null=True,blank=True)
    max_length_or_value=models.CharField(max_length=50,null=True,blank=True)
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.module_name} - {self.label_frontend}"