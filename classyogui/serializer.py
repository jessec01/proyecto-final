#classyogui/serializer.py
from django.db import transaction

from rest_framework import serializers

from .models import ClassYogui

class ClassYoguiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYogui
        fields = ['class_yoga', 'yogui', 'at_creation']
    def create(self, validated_data:dict)->ClassYogui:
        with transaction.atomic():
            class_yogui = ClassYogui.objects.create(**validated_data)
            return class_yogui
    def update(self, instance:ClassYogui, validated_data:dict)->ClassYogui:
        instance.class_yoga = validated_data.get('class_yoga', instance.class_yoga)
        instance.yogui = validated_data.get('yogui', instance.yogui)
        with transaction.atomic():
            instance.save()
        return instance