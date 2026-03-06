#rulespackages/serializer.py

from rest_framework import serializers
from .models import RulePackage
from packages.models import Packages
from rules.models import Rules
class RulePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RulePackage
        fields = ['package', 'rule','at_creation','at_update']
    def validate(self, attrs:dict)->dict:
        package:Packages = attrs.get('package')
        rule:Rules = attrs.get('rule')
        if RulePackage.objects.filter(package=package, rule=rule).exists():
            raise serializers.ValidationError("Rule already exists for this package")
        return attrs