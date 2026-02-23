import re
from rest_framework.serializers import Serializer
from .models import CenterAdministrator
from rest_framework import serializers
from centeryoga.models import YogaCenter
from userYC.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
class CenterAdministratorSerializer(Serializer):
    id=serializers.IntegerField(read_only=True)
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    yoga_center=serializers.PrimaryKeyRelatedField(queryset=YogaCenter.objects.all())
    is_active_profile=serializers.BooleanField(default=True)
    at_creation=serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        user=validated_data.get('user')
        yoga_center=validated_data.get('yoga_center')
        center_administrator=CenterAdministrator.objects.create(
            user=user,
            yoga_center=yoga_center,is_active_profile=validated_data.get('is_active_profile', True)
        )
        return center_administrator
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)   
    def validate_email(self, value):
        email=re.search(r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$',value)
        if not email:
            raise serializers.ValidationError({"email": "invalid email"})
        return value
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError({"password": "Password is required."})
        return value
    def validate(self, attrs):
        return super().validate(attrs)

class CenterAdminTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Una vez validada la contraseña, verificamos el rol
        if not self.user.is_center_administrator:
            raise AuthenticationFailed('No tienes permisos de Administrador de Centro para iniciar sesión aquí.')
        return data
