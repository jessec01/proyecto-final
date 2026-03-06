#classyoga/serializer.py
import re

from datetime import datetime
from django.db import transaction
from django.core.files.base import File

from rest_framework import serializers
from .models import ClassYoga

from centeryoga.serializer import YogaCenterSerializer
from instructor.serializer import InstructorSerializer

class ClassYogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYoga
        fields = ['instructor', 'center', 'name', 'description', 'schedules', 'photo', 'at_creation', 'category']
    def validate_name(self, value:str)->str:
        name=re.search(r'^[a-zA-Z\s]{4,100}$', value)
        if not name:
            raise serializers.ValidationError("invalid name")
        return value    
    def validate_description(self, value:str)->str:
        description=re.search(r'^[a-zA-Z\s]{4,500}$', value)
        if not description:
            raise serializers.ValidationError("invalid description")
        return value    
    def validate_schedules(self, value:dict)->dict:
        #se define un patron de validacion
        required_keys = ['days', 'hour_start', 'hour_end', 'modality']
        #se verifica que todos los campos esten presentes
        for key in required_keys:
            if key not in value:
                raise serializers.ValidationError("invalid schedules")
        #se verifica que 'days' sea una lista
        if not isinstance(value['days'], list):
            raise serializers.ValidationError("'days' must be a list (ej: ['Monday', 'Tuesday'])")
        #se define un patron de validacion para la hora
        time_format = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
        h_inicio = value['hour_start']
        h_fin = value['hour_end']
        #se verifica que la hora tenga el formato correcto
        if not time_format.match(h_inicio) or not time_format.match(h_fin):
            raise serializers.ValidationError("Invalid hour format (HH:MM)")
        start_time = datetime.strptime(h_inicio, "%H:%M")
        end_time = datetime.strptime(h_fin, "%H:%M")
        #se verifica que la hora de inicio sea menor a la hora de fin
        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be less than end time")
        return value   
    def validate_photo(self, value:File)->File:
        if not value.name.endswith('.jpg') and not value.name.endswith('.png'):
           raise serializers.ValidationError("Invalid file format")
        return value
    def validate_category(self, value:str)->str:
        category=re.search(r'^[a-zA-Z\s]{4,100}$', value)
        if not category:
            raise serializers.ValidationError("invalid category")
        return value
    def create(self, validated_data:dict)->ClassYoga:
        with transaction.atomic():
            class_obj = ClassYoga.objects.create(**validated_data)
            return class_obj
    def update(self, instance:ClassYoga, validated_data:dict)->ClassYoga:
        instance.instructor = validated_data.get('instructor', instance.instructor)
        instance.center = validated_data.get('center', instance.center)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.schedules = validated_data.get('schedules', instance.schedules)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.category = validated_data.get('category', instance.category)
        with transaction.atomic():
            instance.save()
        return instance
class ListClassYogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYoga
        fields = ['instructor', 'center', 'name', 'description', 'schedules', 'photo', 'at_creation', 'category']
    def to_representation(self, instance):
        return {
            'instructor': instance.instructor,
            'center': instance.center,
            'name': instance.name,
            'description': instance.description,
            'schedules': instance.schedules,
            'photo': instance.photo,
            'at_creation': instance.at_creation,
            'category': instance.category
        }   
class DetailClassYogaCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYoga
        fields = ['instructor', 'center', 'name', 'description', 'schedules', 'photo', 'at_creation', 'category']
    def to_representation(self, instance):
        return {
            'instructor': instance.instructor,
            'center': instance.center,
            'name': instance.name,
            'description': instance.description,
            'schedules': instance.schedules,
            'photo': instance.photo,
            'at_creation': instance.at_creation,
            'category': instance.category
        }   
    