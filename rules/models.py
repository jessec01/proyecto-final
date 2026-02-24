from django.db import models
from centeryoga.models import YogaCenter    
# Create your models here.
class Rules(models.Model):
    center = models.ForeignKey(YogaCenter, on_delete=models.CASCADE, related_name='rules')
    name = models.CharField(max_length=100)
    description = models.TextField()
    operator=models.CharField(max_length=10,choices=[('+', '+'), ('-', '-'), ('*', '*'), ('/', '/'), ('%', '%')], default='+')
    value=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    active = models.BooleanField(default=True)
    type_rule=models.CharField(max_length=10,choices=[('discount','discount'),('refund','refund'),('surcharge','surcharge'),('fine','fine')], default='discount')
    at_creation = models.DateTimeField(auto_now_add=True)
    at_update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    def apply_rule(self, value):
        if self.operator == '+':
            return value + self.value
        elif self.operator == '-':
            return value - self.value
        elif self.operator == '*':
            return value * self.value
        elif self.operator == '/':
            return value / self.value
        elif self.operator == '%':
            return value % self.value