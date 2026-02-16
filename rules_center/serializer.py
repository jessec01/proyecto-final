import re
from rest_framework import serializers
from .models import Rule
class RuleSerializer(serializers.Serializer):       
    id=serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    active = serializers.BooleanField(default=True)
    at_creation = serializers.DateTimeField(read_only=True)
    def validate_name(self, value):
        name_validation = re.search(r'^[a-zA-Z\s]{4,100}$', value)
        if not name_validation:
            raise serializers.ValidationError({"name": "Name must be between 4 and 100 characters long and contain only letters and spaces."})
        return value
    def validate_description(self, value):
        description_validation = re.search(r'^[a-zA-Z\s]{4,500}$', value)
        if not description_validation:
            raise serializers.ValidationError({"description": "Description must be between 4 and 500 characters long and contain only letters and spaces."})
        return value
    def create(self, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        active = validated_data.get('active')
        rules_center =Rule(name=name, description=description, active=active )
        return rules_center