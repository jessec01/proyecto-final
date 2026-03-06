#centeryoga/serializer.py
#importaciones de librerias
import re

#libreria interna de django
from django.db import transaction

#libreria externa 
from phonenumber_field.phonenumber import to_python
from rest_framework import serializers   

#importaciones de modelos
from .models import YogaCenter

# Serializer for YogaCenter model
class YogaCenterSerializer(serializers.Serializer):
    """ Serializer para el modelo YogaCenter """
    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=100)
    capacity = serializers.IntegerField()
    hours_of_operation = serializers.JSONField()
    photo = serializers.ImageField(max_length=256,        # Longitud máxima del nombre
        allow_empty_file=False, # No permitir archivos vacíos
        use_url=True,           # Devolver URL en lugar del nombre del archivo
        required=False)
    description = serializers.CharField()
    at_creation = serializers   .DateTimeField( read_only=True)
    def validate_code(self, value:str)->str:
        """ Validacion del codigo del centro de yoga """
        code_validation = re.search(r'^[A-Za-z0-9]{4,20}$', value)
        if not code_validation:
            raise serializers.ValidationError({"code": "Code must be between 4 and 20 alphanumeric characters."})
        return value.upper()
    def validate_hours_of_operation(self, value:dict)->dict:
        """ Validacion de las horas de operacion del centro de yoga """
        if not isinstance(value, dict):
            raise serializers.ValidationError({"hours_of_operation": "Hours of operation must be a dictionary."})
        days=value.get('days',"")
        if not re.search(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s,]{4,100}$', days):
            raise serializers.ValidationError({"hours_of_operation": 
            """Hours of operation must contain days, start_time and end_time.
             Format of days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"""})
        start_time=value.get('start_time',"")
        if not re.search(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', start_time):
            raise serializers.ValidationError({"hours_of_operation": 
            """Hours of operation must contain days, start_time and end_time.
             Format of start_time: HH:MM"""})
        end_time=value.get('end_time',"")
        if not re.search(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', end_time):
            raise serializers.ValidationError({"hours_of_operation": 
            """Hours of operation must contain days, start_time and end_time.
             Format of end_time: HH:MM"""}) 
        return value    
    def validate_name(self, value:str)->str:
        """ Validacion del nombre del centro de yoga """
        name_validation = re.search(r'^[\w\sáéíóúÁÉÍÓÚñÑ]{4,100}$', value)
        if not name_validation:
            raise serializers.ValidationError({"name": "Name must be between 4 and 100 characters long and contain only letters and spaces."})
        return value
    def validate_address(self, value:str)->str:
        """ Validacion de la direccion del centro de yoga """
        address_validation = re.search(r'^[\w\s,.\-áéíóúÁÉÍÓÚñÑ+#/()]{10,200}$', value)
        if not address_validation:
            raise serializers.ValidationError({"address": "Address must be between 10 and 200 characters long and can contain letters, numbers, spaces, commas, periods, and hyphens."})
        return value    
    def validate_phone(self, value:str)->str:
        value = to_python(value)
        if YogaCenter.objects.filter(phone=value).exists():
            raise serializers.ValidationError({"phone":"phone number already exists."})
        
        if not value.is_valid():
            raise serializers.ValidationError({"phone":"Invalid phone number."}) 
        return value
    def validate_email(self,value_email:str)->str:
        email=re.search(r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$',value_email)
        if not email:
            raise serializers.  ValidationError({"email": "invalid email"})
        return value_email 
    def validate_photo(self, value_photo:str)->str:
        if value_photo and not value_photo.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError({"photo": "Invalid file type. Only .jpg, .jpeg, and .png are allowed."})
        return value_photo    
    def validate_description(self,value_description:str)->str:
        description=re.search(r'^[\w\s.,;:!¡?¿\'"áéíóúÁÉÍÓÚñÑüÜ()\-+%#&/]{4,500}$',value_description)
        if not description:
            raise serializers.ValidationError({"description": "invalid description"})
        return value_description
    def create(self, validated_data:dict)->YogaCenter:
        code=validated_data.get('code')
        name=validated_data.get('name')
        address=validated_data.get('address')
        phone=validated_data.get('phone')
        email=validated_data.get('email')
        capacity=validated_data.get('capacity')
        hours_of_operation=validated_data.get('hours_of_operation')
        photo=validated_data.get('photo')
        description=validated_data.get('description')
        center = YogaCenter(
                code=code,
                name=name,
                address=address,
                phone=phone,
                email=email,
                capacity=capacity,
                hours_of_operation=hours_of_operation,
                photo=photo,
                description=description
        )
        return center
    def update(self, instance:YogaCenter, validated_data:dict)->YogaCenter:
        instance.code=validated_data.get('code', instance.code)
        instance.name=validated_data.get('name', instance.name)
        instance.address=validated_data.get('address', instance.address)
        instance.phone=validated_data.get('phone', instance.phone)
        instance.email=validated_data.get('email', instance.email)
        instance.hours_of_operation=validated_data.get('hours_of_operation', instance.hours_of_operation)
        instance.photo=validated_data.get('photo', instance.photo)
        instance.description=validated_data.get('description', instance.description)
        instance.save()
        return instance
class ListCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = YogaCenter
        fields = ['id', 'code', 'name', 'capacity', 'address', 'phone', 'email', 'hours_of_operation', 'photo', 'description']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['photo'] = instance.photo.url if instance.photo else None
        representation['hours_of_operation'] = instance.hours_of_operation if instance.hours_of_operation else None
        representation['description'] = instance.description if instance.description else None
        representation['phone'] = instance.phone if instance.phone else None
        representation['email'] = instance.email if instance.email else None
        representation['address'] = instance.address if instance.address else None
        representation['name'] = instance.name if instance.name else None
        return representation
class DetailCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = YogaCenter
        fields = ['id', 'code', 'name', 'capacity', 'address', 'phone', 'email', 'hours_of_operation', 'photo', 'description']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['photo'] = instance.photo.url if instance.photo else None
        representation['hours_of_operation'] = instance.hours_of_operation if instance.hours_of_operation else None
        representation['description'] = instance.description if instance.description else None
        representation['phone'] = instance.phone if instance.phone else None
        representation['email'] = instance.email if instance.email else None
        representation['address'] = instance.address if instance.address else None
        representation['name'] = instance.name if instance.name else None
        return representation   

#serializer para actualizar el centro de yoga
class UpdateCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = YogaCenter
        fields = ['code', 'name', 'capacity', 'address', 'phone', 'email', 'hours_of_operation', 'photo', 'description']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['photo'] = instance.photo.url if instance.photo else None
        representation['hours_of_operation'] = instance.hours_of_operation if instance.hours_of_operation else None
        representation['description'] = instance.description if instance.description else None
        representation['phone'] = instance.phone if instance.phone else None
        representation['email'] = instance.email if instance.email else None
        representation['address'] = instance.address if instance.address else None
        representation['name'] = instance.name if instance.name else None
        return representation  
