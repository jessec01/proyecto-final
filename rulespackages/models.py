from django.db import models
from packages.models import Packages
from rules.models import Rules
# Create your models here.
class RulePackage(models.Model):
    package=models.ForeignKey(Packages, on_delete=models.CASCADE)
    rule=models.ForeignKey(Rules, on_delete=models.CASCADE)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['package', 'rule'], 
                                    name='unique_rule_package')
        ]   
    def __str__(self):
        return f'{self.package} - {self.rule}'
