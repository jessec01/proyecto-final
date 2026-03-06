#packagessubscription/models.py

#Importaciones django
from django.db import models

#Importaciones internas
from packages.models import Packages
from subscription.models import Subscription
# Create your models here.
class PackageSubscription(models.Model):
    package=models.ForeignKey(Packages, on_delete=models.CASCADE)
    subscription=models.ForeignKey(Subscription, on_delete=models.CASCADE)
    class_remaining=models.IntegerField()
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['package','subscription'], name='unique_package_subscription')
        ]
    def __str__(self):
        return f'{self.package} - {self.subscription}'
