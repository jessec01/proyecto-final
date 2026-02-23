from rest_framework import serializers
from .models import RulesPayment
from rules_center.models import RulesCenter
class RulesPaymentSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    discoint_porcentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    comission_porcentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    rules_center=serializers.PrimaryKeyRelatedField(queryset=RulesCenter.objects.all(), write_only=True)
    def validate_discoint_porcentage(self, value):
        value=float(value)
        if value < 0 or value > 100:
            raise serializers.ValidationError({"discoint_porcentage": "Discount percentage must be between 0 and 100."})
        return value
    
    def validate_comission_porcentage(self, value):
        value=float(value)
        if value < 0 or value > 100:
            raise serializers.ValidationError({"comission_porcentage": "Comission percentage            must be between 0 and 100.  "})
        return value
    def create(self, validated_data):
        rules_center = validated_data.get('rules_center'),
        discoint_porcentage = validated_data.get('discoint_porcentage')
        comission_porcentage = validated_data.get('comission_porcentage')
        rules_payment = RulesPayment(rules_center=rules_center, discoint_porcentage=discoint_porcentage, comission_porcentage=comission_porcentage)
        return rules_payment
    