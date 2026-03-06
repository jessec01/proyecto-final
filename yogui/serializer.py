from rest_framework import serializers
from .models import Yogui
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
class YoguiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yogui
        fields = ['id', 'user', 'id_card', 'level_suscribed', 'photo_profile'] 
        read_only_fields = ['user']
    def create(self, validated_data):
        return super().create(validated_data)
class ReadLoginFormSerializer(serializers.Serializer):
    class Meta:
        model = Yogui
        fields = ['email','password']
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


class YoguiTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Una vez validada la contraseña, verificamos el rol
        if not self.user.is_yogui:
            raise AuthenticationFailed('No tienes permisos de Yogui para iniciar sesión aquí.')
        return data
