from django.db import models
from  policy.models import Policy
from promotion.models import Promotion
# Create your models here.
class Pay(models.Model):
    policy=models.ForeignKey(Policy, on_delete=models.CASCADE)
    promotion=models.ForeignKey(Promotion, on_delete=models.CASCADE)
    original_amount=models.DecimalField(max_digits=10, decimal_places=2)
    final_amount=models.DecimalField(max_digits=10, decimal_places=2)
    paymend_detail=models.JSONField()
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.policy} - {self.final_amount}'  