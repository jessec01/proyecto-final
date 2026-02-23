from django.db import models

from rules_center.models import RulesCenter
# Create your models here.
class Packages(models.Model):
    rule_center=models.ForeignKey(RulesCenter,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    duration=models.IntegerField()
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    