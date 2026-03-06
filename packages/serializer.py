#packages/serializer.py
import re
from django.db import transaction
from rest_framework import serializers

from .models import Packages

class PackagesSerializer(serializers.Serializer):
    """Serializer for Packages model"""
    name=serializers.CharField(max_length=100)
    description=serializers.CharField(max_length=100)
    price=serializers.DecimalField(max_digits=10, decimal_places=2)
    duration=serializers.JSONField()
    level_package=serializers.ChoiceField(choices=[('beginner','beginner'),('intermediate','intermediate'),('advanced','advanced')], default='beginner')
    category=serializers.ChoiceField(choices=[('monthly','monthly'),('yearly','yearly'),('single','single')], default='monthly')
    stackclass=serializers.ChoiceField(choices=[('suscription','999'),('packages','10'),('class','1')], default='class')
    at_creation=serializers.DateTimeField(read_only=True)
    at_update=serializers.DateTimeField(read_only=True)

    def validate_name(self, value: str) -> str:
        """Validate name"""
        if not re.match(r'^[\w\sáéíóúÁÉÍÓÚñÑ]+$', value):
            raise serializers.ValidationError('Name must contain valid characters')
        return value

    def validate_description(self, value: str) -> str:
        """Validate description"""
        if not re.match(r'^[\w\s.,;:!¡?¿\'"áéíóúÁÉÍÓÚñÑüÜ()\-+%#&/]+$', value):
            raise serializers.ValidationError('Description must contain valid characters')
        return value

    def validate_price(self, value) -> float:
        """Validate price"""
        try:
            val = float(value)
        except ValueError:
            raise serializers.ValidationError('Price must be a valid number')
            
        if val < 0:
            raise serializers.ValidationError('Price must be positive')
        return val

    def validate_duration(self, value) -> dict:
        """Validate duration"""
        if not isinstance(value, dict):
            raise serializers.ValidationError('Duration must be a JSON object')
        return value

    def create(self, validated_data: dict) -> Packages:
        """Create a new package"""
        package = Packages(**validated_data)
        with transaction.atomic():
            package.save()
        return package

    def update(self, instance: Packages, validated_data: dict) -> Packages:
        """Update a package"""
        instance.name=validated_data.get('name', instance.name)
        instance.description=validated_data.get('description', instance.description)
        instance.price=validated_data.get('price', instance.price)
        instance.duration=validated_data.get('duration', instance.duration)
        instance.level_package=validated_data.get('level_package', instance.level_package)
        instance.category=validated_data.get('category', instance.category)
        instance.stackclass=validated_data.get('stackclass', instance.stackclass)
        with transaction.atomic():
            instance.save()
        return instance

class PackagesListSerializer(serializers.ModelSerializer):
    """Serializer for Packages model"""
    class Meta:
        model = Packages
        fields = ['name', 'description', 'price', 'duration', 'level_package', 'category', 'stackclass']

    def to_representation(self, instance: Packages) -> dict:
        """ Serializador para la lista de paquetes """
        return {
            'name': instance.name,
            'description': instance.description,
            'price': instance.price,
            'duration': instance.duration,
            'level_package': instance.level_package,
            'category': instance.category,
            'stackclass': instance.stackclass
        }

class PackagesDetailSerializer(serializers.ModelSerializer):
    """Serializer for Packages model"""
    class Meta:
        model = Packages
        fields = ['name', 'description', 'price', 'duration', 'level_package', 'category', 'stackclass']

    def to_representation(self, instance: Packages) -> dict:
        """ Serializador para el detalle de paquetes """
        return {
            'name': instance.name,
            'description': instance.description,
            'price': instance.price,
            'duration': instance.duration,
            'level_package': instance.level_package,
            'category': instance.category,
            'stackclass': instance.stackclass
        }
