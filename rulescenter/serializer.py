#rulescenter/serializer.py
from rest_framework import serializers
from .models import RuleCenter

class RuleCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleCenter
        fields = ['center', 'rule']
    def validate(self, attrs):
        center = attrs.get('center')
        rule = attrs.get('rule')
        if RuleCenter.objects.filter(center=center, rule=rule).exists():
            raise serializers.ValidationError("Rule already exists for this center")
        return attrs
