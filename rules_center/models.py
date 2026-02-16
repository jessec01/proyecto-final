from django.db import models
from centeryoga.models import YogaCenter    
# Create your models here.
class Rule(models.Model):
    center = models.ForeignKey(YogaCenter, on_delete=models.CASCADE, related_name='rules')
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)
    at_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name