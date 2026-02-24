#policy/serializer.py
from django.db import transaction
from rest_framework import serializers

from .models import Policy

class PolicySerializer(serializers.Serializer):
    """Serializer for Policy model"""
    id=serializers.IntegerField(read_only=True)
    is_refundable=serializers.BooleanField(default=False)
    is_transferable=serializers.BooleanField(default=False)
    is_discountable=serializers.BooleanField(default=False)
    is_acumulative=serializers.BooleanField(default=False)
    is_active_suspension=serializers.BooleanField(default=False)
    at_creation=serializers.DateTimeField(read_only=True)
    at_update=serializers.DateTimeField(read_only=True)

    def create(self, validated_data:dict)->Policy:
        """Create a new policy"""
        policy = Policy(**validated_data)
        with transaction.atomic():
            policy.save()
        return policy

    def update(self, instance:Policy, validated_data:dict)->Policy:
        """Update a policy"""
        instance.is_refundable=validated_data.get('is_refundable', instance.is_refundable)
        instance.is_transferable=validated_data.get('is_transferable', instance.is_transferable)
        instance.is_discountable=validated_data.get('is_discountable', instance.is_discountable)
        instance.is_acumulative=validated_data.get('is_acumulative', instance.is_acumulative)
        instance.is_active_suspension=validated_data.get('is_active_suspension', instance.is_active_suspension)
        with transaction.atomic():    
            instance.save()
        return instance

class PolicyListSerializer(serializers.ModelSerializer):
    """Serializer for Policy model"""
    class Meta:
        model = Policy
        fields = ['is_refundable', 'is_transferable', 'is_discountable', 'is_acumulative', 'is_active_suspension', 'at_creation', 'at_update']

    def to_representation(self, instance:Policy)->dict:
        """ Serializador para la lista de politicas """
        return {
            'is_refundable': instance.is_refundable,
            'is_transferable': instance.is_transferable,
            'is_discountable': instance.is_discountable,
            'is_acumulative': instance.is_acumulative,
            'is_active_suspension': instance.is_active_suspension,
            'at_creation': instance.at_creation,
            'at_update': instance.at_update
        }

class PolicyDetailSerializer(serializers.ModelSerializer):
    """Serializer for Policy model"""
    class Meta:
        model = Policy
        fields = [ 'is_refundable', 'is_transferable', 'is_discountable', 'is_acumulative', 'is_active_suspension', 'at_creation', 'at_update']

    def to_representation(self, instance:Policy)->dict:
        """ Serializador para el detalle de politicas """
        return {
            'is_refundable': instance.is_refundable,
            'is_transferable': instance.is_transferable,
            'is_discountable': instance.is_discountable,
            'is_acumulative': instance.is_acumulative,
            'is_active_suspension': instance.is_active_suspension,
            'at_creation': instance.at_creation,
            'at_update': instance.at_update
        }