#attendace/serializer.py
#importaciones de django
from django.utils import timezone   
#importaciones de rest_framework
from rest_framework import serializers
#importaciones internas
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer para Attendance.
    """
    class Meta:
        model = Attendance
        fields = ['session', 'yogui', 'status']
        read_only_fields = ('yogui',)   
    def validate(self, attrs):
        """
        Valida que la asistencia sea válida.
        """
        session = attrs.get('session')
        yogui = attrs.get('yogui')
        status = attrs.get('status')
        if session.date < timezone.now().date():
            raise serializers.ValidationError("La sesión ya pasó.")
        if session.start_time < timezone.now().time() and session.date == timezone.now().date():
            raise serializers.ValidationError("La sesión ya empezó.")
        if session.end_time < timezone.now().time() and session.date == timezone.now().date():
            raise serializers.ValidationError("La sesión terminó.")
        if status not in ['PRESENT', 'ABSENT', 'PENDING']:
            raise serializers.ValidationError("Estado de asistencia inválido.")
        return attrs
    def create(self, validated_data):
        """
        Crea una nueva asistencia.
        """
        return Attendance.objects.create(**validated_data)    
    def update(self, instance, validated_data):
        """
        Actualiza una asistencia existente.
        """
        instance.session = validated_data.get('session', instance.session)
        instance.yogui = validated_data.get('yogui', instance.yogui)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
