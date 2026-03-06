#rulespayment/serializer.py
from rest_framework import serializers
from .models import RulePay
from pay.models import Pay
from rules.models import Rules
class RulePaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RulePay
        fields = ['pay', 'rule']
    def validate(self, attrs:dict)->dict:
        pay:Pay = attrs.get('pay')
        rule:Rule = attrs.get('rule')
        if RulePay.objects.filter(pay=pay, rule=rule).exists():
            raise serializers.ValidationError("Rule already exists for this pay")
        return attrs