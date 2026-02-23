from rest_framework import serializers
from .models import RulesPackages   
from rules_center.models import RulesCenter
class RulesPackagesSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    promotion_porcentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    access_duration = serializers.IntegerField()
    rules_center=serializers.PrimaryKeyRelatedField(queryset=RulesCenter.objects.all(), write_only=True)
    def validate_promotion_porcentage(self, value):
        value=float(value)
        if value < 0 or value > 100:
            raise   serializers.ValidationError({"promotion_percentage": "Promotion percentage must be between 0 and 100."})
        return value
    def validate_access_duration(self, value):
        value=int(value)
        if value <= 0:
            raise serializers.ValidationError({"access_duration": "Access duration must be a positive integer."})
        return value
    def create(self, validated_data):
        rules_center = validated_data.get('rules_center')
        promotion_porcentage = validated_data.get('promotion_porcentage')
        access_duration = validated_data.get('access_duration')
        rules_packages = RulesPackages(rules_center=rules_center, promotion_porcentage=promotion_porcentage, access_duration=access_duration)
        return rules_packages
    