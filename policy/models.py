from django.db import models

# Create your models here.
class Policy(models.Model):
    is_refundable=models.BooleanField(default=False)
    is_transferable=models.BooleanField(default=False)
    is_discountable=models.BooleanField(default=False)
    is_acumulative=models.BooleanField(default=False)
    is_active_suspension=models.BooleanField(default=False)
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
