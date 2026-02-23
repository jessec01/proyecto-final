from django.db import models
from rules_center.models import RulesCenter
# Create your models here.
class RulesPayment(RulesCenter):
    rules_center = models.ForeignKey(RulesCenter, on_delete=models.CASCADE, related_name='rules_payment')
    discoint_porcentage = models.DecimalField(max_digits=5, decimal_places=2)
    comission_porcentage = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.name