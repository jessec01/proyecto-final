from django.db import models

from rules.models import Rules
# Create your models here.
class Packages(models.Model):
    center = models.ForeignKey('centeryoga.YogaCenter', on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    duration=models.JSONField()
    level_package=models.CharField(max_length=20,choices=[('beginner','beginner'),('intermediate','intermediate'),('advanced','advanced')], default='beginner')
    category=models.CharField(max_length=20,choices=[('monthly','monthly'),('yearly','yearly'),('single','single')], default='monthly')
    stackclass=models.CharField(max_length=20,choices=[('suscription','999'),('packages','10'),('class','1')], default='class')
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    