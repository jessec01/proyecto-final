#pay/models.py
#importaciones django
from django.db import models

#importaciones internas
from packages.models import Packages
from  policy.models import Policy
from promotion.models import Promotion
from yogui.models import Yogui

# Create your models here.
class Pay(models.Model):
    yogui=models.ForeignKey(Yogui, on_delete=models.CASCADE,null=True,blank=True)
    package=models.ForeignKey(Packages, on_delete=models.CASCADE,null=True,blank=True)
    policy=models.ForeignKey(Policy, on_delete=models.CASCADE)
    promotion=models.ForeignKey(Promotion, null=True, blank=True, on_delete=models.CASCADE)
    original_amount=models.DecimalField(max_digits=10, decimal_places=2)
    final_amount=models.DecimalField(max_digits=10, decimal_places=2)
    paymend_detail=models.JSONField()
    #detalle de pago no recuerdo que iba aqui
    status=models.BooleanField(default=True)
    at_creation=models.DateTimeField(auto_now_add=True)
    at_update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.policy} - {self.final_amount}' 
    def restriction_pay(self)->bool:
        return self.policy.restriction_pay()
    def status_pay(self)->bool:
        return self.status
    def activate_pay(self):
        self.status=True
        self.save()
    def deactivate_pay(self):
        self.status=False
        self.save()
    def pay_promocion(self):
        self.final_amount=(self.final_amount *self.promotion.price)/100
        self.save()