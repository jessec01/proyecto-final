#rulescenter/models.py
from django.db import models

from  centeryoga.models import CenterYoga
from rules.models import Rule
# Create your models here.
class RuleCenter(models.Model):
    center=models.ForeignKey(CenterYoga, on_delete=models.CASCADE)
    rule=models.ForeignKey(Rule, on_delete=models.CASCADE)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['center', 'rule'], 
                                    name='unique_rule_center')
        ]   
    def __str__(self):
        return f'{self.center} - {self.rule}'
    