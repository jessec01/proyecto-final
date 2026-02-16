from django.db import models
from rules_center.models import Rule
# Create your models here.
class RulesPackages(Rule):
    rules_center = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='rules_packages')
    promotion_porcentage = models.DecimalField(max_digits=5, decimal_places=2)
    access_duration = models.PositiveIntegerField(help_text="Duration in days")
    def __str__(self):
        return self.name