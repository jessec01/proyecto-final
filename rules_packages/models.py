from django.db import models
from rules_center.models import RulesCenter
# Create your models here.
class RulesPackages(RulesCenter):
    rules_center = models.ForeignKey(RulesCenter, on_delete=models.CASCADE, related_name='rules_packages')
    promotion_porcentage = models.DecimalField(max_digits=5, decimal_places=2)
    access_duration = models.PositiveIntegerField(help_text="Duration in days")
    def __str__(self):
        return self.name