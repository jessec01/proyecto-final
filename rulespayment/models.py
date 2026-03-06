from django.db import models

from pay.models import Pay
from rules.models import Rules
# Create your models here.
class RulePay(models.Model):
    pay=models.ForeignKey(Pay, on_delete=models.CASCADE)
    rule=models.ForeignKey(Rules, on_delete=models.CASCADE)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['pay', 'rule'], 
                                    name='unique_rule_pay')
        ]   
    def __str__(self):
        return f'{self.pay} - {self.rule}'
