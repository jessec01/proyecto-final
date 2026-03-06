#classsession/serializer.py
#importaciones de django
from django.utils import timezone
#importaciones de rest_framework
from rest_framework import serializers
#importaciones internas
from .models import ClassSession

class ClassSessionSerializer(serializers.ModelSerializer):
    """
    Serializer para ClassSession.
    """
    class Meta:
        model = ClassSession
        fields = ['class_yoga', 'instructor', 'center', 'date', 'start_time', 'end_time']
        read_only_fields = ('instructor', 'center')
    def validate(self, attrs):
        """
        Valida que la sesión sea válida.
        """
        date = attrs.get('date')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        if date < timezone.now().date():
            raise serializers.ValidationError("La fecha no puede ser pasada.")
        if start_time < timezone.now().time() and date == timezone.now().date():
            raise serializers.ValidationError("La hora de inicio no puede ser pasada.")
        if start_time >= end_time:
            raise serializers.ValidationError("La hora de inicio no puede ser mayor o igual a la hora de fin.")
        if end_time < timezone.now().time() and date == timezone.now().date():
            raise serializers.ValidationError("La hora de fin no puede ser pasada.")
        return attrs
    def create(self, validated_data):
        """
        Crea una nueva sesión.
        """
        return ClassSession.objects.create(**validated_data)    
    def update(self, instance, validated_data):
        """
        Actualiza una sesión existente.
        """
        instance.class_yoga = validated_data.get('class_yoga', instance.class_yoga)
        instance.instructor = validated_data.get('instructor', instance.instructor)
        instance.center = validated_data.get('center', instance.center)
        instance.date = validated_data.get('date', instance.date)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.save()
        return instance
class ClassSessionListSerializer(serializers.ModelSerializer):
    """
    Serializer para listar ClassSession.
    """
    class Meta:
        model = ClassSession
        fields = ['id', 'class_yoga', 'instructor', 'center', 'date', 'start_time', 'end_time']
        read_only_fields = ('instructor', 'center')
    def to_representation(self, instance):
        """
        Convierte la representación de la sesión.
        """
        representation = super().to_representation(instance)
        representation['instructor'] = self.get_instructor(instance)
        representation['center'] = self.get_center(instance)
        representation['class_yoga'] = self.get_class_yoga(instance)
        return representation
    def get_instructor(self, obj):
        """Devuelve el instructor de la sesión."""
        return obj.instructor.username
    def get_center(self, obj):
        """Devuelve el centro de la sesión."""
        return obj.center.name
    def get_class_yoga(self, obj):
        """Devuelve el tipo de clase de la sesión."""
    
class ClassSessionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para detallar ClassSession.
    """
    class Meta:
        model = ClassSession
        fields = ['id', 'class_yoga', 'instructor', 'center', 'date', 'start_time', 'end_time']
        read_only_fields = ('instructor', 'center')
    def to_representation(self, instance):
        """
        Convierte la representación de la sesión.
        """
        representation = super().to_representation(instance)
        representation['instructor'] = self.get_instructor(instance)
        representation['center'] = self.get_center(instance)
        representation['class_yoga'] = self.get_class_yoga(instance)
        return representation
    def get_instructor(self, obj):
        """Devuelve el instructor de la sesión."""
        return obj.instructor.username
    def get_center(self, obj):
        """Devuelve el centro de la sesión."""
        return obj.center.name
    def get_class_yoga(self, obj):
        """Devuelve el tipo de clase de la sesión."""
    
    return obj.class_yoga.name  