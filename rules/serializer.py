#rules/serializer.py
import re

from django.db import transaction

from rest_framework import serializers

from .models import Rules
class RulesSerializer(serializers.Serializer):       
    """Serializer for Rules model"""
    id=serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    operator=serializers.CharField(write_only=True)
    value=serializers.DecimalField(max_digits=10, decimal_places=2,default=0)
    active = serializers.BooleanField(default=True)
    type_rule=serializers.CharField(write_only=True)
    at_creation = serializers.DateTimeField(read_only=True)
    def validate_name(self, value:str)->str:
        name_validation = re.search(r'^[a-zA-Z\s]{4,100}$', value)
        if not name_validation:
            raise serializers.ValidationError({"name": "Name must be between 4 and 100 characters long and contain only letters and spaces."})
        return value
    def validate_description(self, value:str)->str:
        description_validation = re.search(r'^[a-zA-Z\s]{4,500}$', value)
        if not description_validation:
            raise serializers.ValidationError({"description": "Description must be between 4 and 500 characters long and contain only letters and spaces."})
        return value
    def create(self, validated_data:dict)->Rules:
        name = validated_data.get('name')
        description = validated_data.get('description')
        operator = validated_data.get('operator')
        value = validated_data.get('value')
        active = validated_data.get('active')
        type_rule = validated_data.get('type_rule')
        rules = Rules(name=name, description=description, operator=operator, value=value, active=active, type_rule=type_rule)
        rules.save()
        return rules
class RulesUpdateSerializer(serializers.Serializer):
    """Serializer for Rules model"""
    id=serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    operator=serializers.CharField(write_only=True)
    value=serializers.DecimalField(max_digits=10, decimal_places=2,default=0)
    active = serializers.BooleanField(default=True)
    type_rule=serializers.CharField(write_only=True)
    at_creation = serializers.DateTimeField(read_only=True)
    def validate_name(self, value:str)->str:
        name_validation = re.search(r'^[a-zA-Z\s]{4,100}$', value)
        if not name_validation:
            raise serializers.ValidationError({"name": "Name must be between 4 and 100 characters long and contain only letters and spaces."})
        return value
    def validate_description(self, value:str)->str:
        description_validation = re.search(r'^[a-zA-Z\s]{4,500}$', value)
        if not description_validation:
            raise serializers.ValidationError({"description": "Description must be between 4 and 500 characters long and contain only letters and spaces."})
        return value
    def update(self, instance:Rules, validated_data:dict)->Rules:
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.operator = validated_data.get('operator', instance.operator)
        instance.value = validated_data.get('value', instance.value)
        instance.active = validated_data.get('active', instance.active)
        instance.type_rule = validated_data.get('type_rule', instance.type_rule)
        with transaction.atomic():
            instance.save()
        return instance
class  RulesListSerializer(serializers.ModelSerializer):
    """Serializer para la lista de reglas"""
    class Meta:
        model = Rules
        fields = ['name', 'description', 'operator', 'value', 'active', 'type_rule', 'at_creation']
    def to_representation(self, instance:Rules)->dict:
        """ Serializador para la lista de reglas """
        return {
            'name': instance.name,
            'description': instance.description,
            'operator': instance.operator,
            'value': instance.value,
            'active': instance.active,
            'type_rule': instance.type_rule,
            'at_creation': instance.at_creation
        }
class RulesDetailSerializer(serializers.ModelSerializer):
    """Serializer para el detalle de reglas"""
    class Meta:
        model = Rules
        fields = ['name', 'description', 'operator', 'value', 'active', 'type_rule', 'at_creation']
    def to_representation(self, instance:Rules)->dict:
        """ Serializador para el detalle de reglas """
        return {
            'name': instance.name,
            'description': instance.description,
            'operator': instance.operator,
            'value': instance.value,
            'active': instance.active,
            'type_rule': instance.type_rule,
            'at_creation': instance.at_creation
        }