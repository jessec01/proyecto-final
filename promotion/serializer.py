#promotion/serializer.py
import re
from django.db import transaction
from rest_framework import serializers

from .models import Promotion

class PromotionSerializer(serializers.Serializer):
    """Serializer for Promotion model"""
    name=serializers.CharField(max_length=100)
    description=serializers.CharField(max_length=100)
    discount_type=serializers.CharField(max_length=100)
    discount_value=serializers.FloatField(default=0)
    active=serializers.BooleanField(default=True)
    at_creation=serializers.DateTimeField(read_only=True)
    at_update=serializers.DateTimeField(read_only=True)

    def validate_name(self, value: str) -> str:
        """Validate name"""
        if not re.match(r'^[\w\sáéíóúÁÉÍÓÚñÑ]+$', value):
            raise serializers.ValidationError('Name must contain only letters and numbers')
        return value

    def validate_description(self, value: str) -> str:
        """Validate description"""
        if not re.match(r'^[\w\s.,;:!¡?¿\'"áéíóúÁÉÍÓÚñÑüÜ()\-+%#&/]+$', value):
            raise serializers.ValidationError('Description must contain valid characters')
        return value

    def validate_discount_value(self, value) -> float:
        """Validate discount value"""
        try:
            val = float(value)
        except ValueError:
            raise serializers.ValidationError('Discount value must be a valid number')
            
        if val < 0:
            raise serializers.ValidationError('Discount value must be positive')
        elif val > 100:
            raise serializers.ValidationError('Discount value must be less than or equal to 100')
        return val

    def create(self, validated_data: dict) -> Promotion:
        """Create a new promotion"""
        promotion = Promotion(**validated_data)
        with transaction.atomic():
            promotion.save()
        return promotion

    def update(self, instance: Promotion, validated_data: dict) -> Promotion:
        """Update a promotion"""
        instance.name=validated_data.get('name', instance.name)
        instance.description=validated_data.get('description', instance.description)
        instance.discount_type=validated_data.get('discount_type', instance.discount_type)
        instance.discount_value=validated_data.get('discount_value', instance.discount_value)
        instance.active=validated_data.get('active', instance.active)
        with transaction.atomic():
            instance.save()
        return instance

class PromotionListSerializer(serializers.ModelSerializer):
    """Serializer for Promotion model"""
    class Meta:
        model = Promotion
        fields = ['name', 'description', 'discount_type', 'discount_value', 'active']

    def to_representation(self, instance: Promotion) -> dict:
        """ Serializador para la lista de promociones """
        return {
            'name': instance.name,
            'description': instance.description,
            'discount_type': instance.discount_type,
            'discount_value': instance.discount_value,
            'active': instance.active
        }

class PromotionDetailSerializer(serializers.ModelSerializer):
    """Serializer for Promotion model"""
    class Meta:
        model = Promotion
        fields = ['name', 'description', 'discount_type', 'discount_value', 'active']

    def to_representation(self, instance: Promotion) -> dict:
        """ Serializador para el detalle de promociones """
        return {
            'name': instance.name,
            'description': instance.description,
            'discount_type': instance.discount_type,
            'discount_value': instance.discount_value,
            'active': instance.active
        }