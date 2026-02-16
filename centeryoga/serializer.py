import re
from rest_framework import serializers   

from .models import YogaCenter
from phonenumber_field.phonenumber import to_python
from rules_center.serializer import RuleSerializer
from rules_center.models import Rule
from rules_payments.serializer import RulesPaymentSerializer
from rules_payments.models import RulesPayment
from rules_packages.serializer import RulesPackagesSerializer
from rules_packages.models import RulesPackages
from center_administration.models import CenterAdministrator
from center_administration.serializer import CenterAdministratorSerializer
from django.db import transaction

# Serializer for YogaCenter model
class CenterSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=100)
    capacity = serializers.IntegerField()
    photo = serializers.ImageField(max_length=256,        # Longitud máxima del nombre
        allow_empty_file=False, # No permitir archivos vacíos
        use_url=True,           # Devolver URL en lugar del nombre del archivo
        required=False)
    
    description = serializers.CharField()
    at_creation = serializers   .DateTimeField( read_only=True)
    def validate_code(self, value):
        code_validation = re.search('^[A-Z0-9]{10}$', value)
        if not code_validation:
            raise serializers.ValidationError({"code": "Code must be 10 characters long and contain only uppercase letters and numbers."})
        return value
    def validate_name(self, value):
        name_validation = re.search(r'^[a-zA-Z\s]{4,100}$', value)
        if not name_validation:
            raise serializers.  ValidationError({"name": "Name must be between 4 and 100 characters long and contain only letters and spaces."})
        return value
    def validate_address(self, value):
        #para actualizaciones futuras se pueden agregar validaciones mas especificas dependiendo de las politicas del centro de yoga
        #ademas de restricciones con validacion de localidades reales
        address_validation = re.search(r'^[a-zA-Z0-9\s,.-]{10,200}$', value)
        if not address_validation:
            raise serializers.ValidationError({"address": "Address must be between 10 and 200 characters long and can contain letters, numbers, spaces, commas, periods, and hyphens."})
        return value    
    def validate_phone(self, value):
        value = to_python(value)
        if YogaCenter.objects.filter(phone=value).exists():
            raise serializers.ValidationError({"phone":"phone number already exists."})
        
        if not value.is_valid():
            raise serializers.ValidationError({"phone":"Invalid phone number."}) 
        return value
    def validate_email(self,value_email):
        email=re.search(r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$',value_email)
        if not email:
            raise serializers.  ValidationError({"email": "invalid email"})
        return value_email 
    def validate_capacity(self, value):
        #se asegura que la capacidad sea un número positivo
        #para futuras actualizaciones la capacidad dependera de la politicas definidas del centros 
        if value <= 0:
            raise serializers.ValidationError({"capacity": "Capacity must be a positive integer."})
        return value
    def validate_photo(self, value_photo):
        if value_photo and not value_photo.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError({"photo": "Invalid file type. Only .jpg, .jpeg, and .png are allowed."})
        return value_photo    
    def validate_description(self,value_description):
        description=re.search(r'^[a-zA-Z\s]{4,500}$',value_description)
        if not description:
            raise   serializers.        ValidationError({"description": "invalid description"})
        return value_description
    def create(self, validated_data):
        code=validated_data.get('code')
        name=validated_data.get('name')
        address=validated_data.get('address')
        phone=validated_data.get('phone')
        email=validated_data.get('email')
        capacity=validated_data.get('capacity')
        photo=validated_data.get('photo')
        description=validated_data.get('description')

        
        center = YogaCenter(
                code=code,
                name=name,
                address=address,
                phone=phone,
                email=email,
                capacity=capacity,
                photo=photo,
                description=description
        )
        return center
    
class MasterSerializer(serializers.Serializer):
    center=CenterSerializer()
    rules_center =  RuleSerializer()
    rules_packages = RulesPackagesSerializer()
    rules_payments = RulesPaymentSerializer()
    center_administrator = CenterAdministratorSerializer()
    def create(self, validated_data):
        #extraccion de la informacion de las reglas y del administrador del centro para crear las instancias correspondientes antes de crear el centro de yoga, esto se hace para asegurar la integridad de los datos y las relaciones entre las diferentes entidades del sistema.
        user=validated_data.pop('user')
        center=validated_data.pop('center')
        admin_center_data = validated_data.pop('center_administrator')
        rules_center_data = validated_data.pop('rules_center')
        rules_packages_data = validated_data.pop('rules_packages')
        rules_payments_data = validated_data.pop('rules_payments')
        #creacion de los modelos dependientes antes de crear el centro de yoga
        with transaction.atomic():
           
            yoga_center=YogaCenter.objects.create(**center)
            
            center_administrator = CenterAdministrator.objects.create(user=user, **admin_center_data)
            
            object_rules_center = Rule.objects.create(center=yoga_center, **rules_center_data)
            object_rules_packages = RulesPackages.objects.create(rules_center=object_rules_center, **rules_packages_data)
            object_rules_payments = RulesPayment.objects.create(rules_center=object_rules_center, **rules_payments_data)
            #modificar el estado center para que se active una vez que se hayan creado todas las entidades relacionadas                                                
            center_administrator.activate_profile()
            return yoga_center
    