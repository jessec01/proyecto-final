#pay/service.py
#
from datetime import timedelta
#importaciones de django
from django.db import transaction
from django.utils import timezone

#importaciones internas
from packages.models import Packages 
from packagessubscription.models import PackageSubscription
from pay.models import Pay
from promotion.models import Promotion
from policy.models import Policy
from subscription.models import Subscription
from yogui.models import Yogui

#from subscription
class PayService:
  """ maneja la logica de negocio del pago"""
  def process_pay(self,yogui:Yogui,package:Packages):
    #valida que exista un paquete activo vinculado al yogui
    #igual a una consulta JOIN en postgres 
    #valida que el yogui este subcrito 
    if yogui.is_suscribed:
        raise Exception("El yogui ya tiene una suscripcion activa")
        #al validar primero si el yogui esta subcrito reducimos la consulta 
        #de validacion del paquete
        #validamos que el paquete este activo usando consulta
    packages_active:bool=PackageSubscription.objects.filter(
        package=package,
        subscription__yogui=yogui,
        subscription__date_end__gte=timezone.now().date(),
        class_remaining__gt=0
    ).exists()
    #validamos que el paquete este activo si esta  lanzamos un exception
    if packages_active:
        raise Exception("El paquete ya tiene una suscripcion activa")
        #buscamos la  promocion al paquete que se va va a comprar
        #se  busca para no volver  a consultar
    promotion:Promotion=Promotion.objects.filter(center=package.center,
        active=True).first()
    policy=Policy.objects.filter(center=package.center).first()
    #definimos una variable para decirle al transacionn si hubo
    #descuento o no
    is_promotion:bool=True if promotion else False
    #validamos que la promocion existe
    price_base:float=package.price
    price_final=price_base
    if is_promotion:
        #ubicamos si esta activo
        #rescatamos el valor del descuento
        promotion_value_active:float=promotion.discount_value
        #obtenemos el precio base
     
        #calculamos el descuento en precio
        price_discount:float=package.price*promotion_value_active/100
        #calculamos el precio final
        price_final:float=price_base-price_discount
    #no importa si promocion y no lo importante es persitencia del pago
    #si solo anexamos la funcion los parametro del precio
    #que cambia de acuerdo a la promocion
    #no queda un sistema como una llamada
    namepackage=package.name 
    paymend_detail={'compra de paquete':f'{namepackage}'}
    with transaction.atomic():
        pay=Pay.objects.create(policy=policy,promotion=promotion,
            yogui=yogui,package=package,original_amount=price_base,
            final_amount=price_final,paymend_detail=paymend_detail
        )
        subscription=Subscription.objects.create(yogui=yogui,
        date_start=timezone.now().date(),
        date_end=timezone.now().date()+timedelta(days=package.duration.get('days',30)
        ))
        packagesubcription=PackageSubscription.objects.create(
             package=package,
             subscription=subscription,
             class_remaining=int(package.stackclass) if package.stackclass.isdigit() else 
             1
        )
        yogui.update_is_suscribed()
        yogui.update_level_suscribed(package.level_package)
        return pay

      
  