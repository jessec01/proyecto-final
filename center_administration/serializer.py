import re
from rest_framework.serializers import Serializer
from .models import CenterAdministrator
from rest_framework import serializers
from centeryoga.models import YogaCenter
from userYC.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
#Serializador para el modelo CenterAdministrator
class CenterAdministratorSerializer(Serializer):
    """
    Serializador para el modelo CenterAdministrator
    Se usa Serializer en vez de ModelSerializer porque no se va a crear el modelo en la base de datos   
    Se usa para crear el perfil del administrador
    """ 
    id=serializers.IntegerField(read_only=True)
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    yoga_center=serializers.PrimaryKeyRelatedField(queryset=YogaCenter.objects.all())
    is_active_profile=serializers.BooleanField(default=True)
    at_creation=serializers.DateTimeField(read_only=True)
    photo_profile=serializers.ImageField(allow_null=True, required=False)
    role=serializers.CharField(max_length=50, allow_null=True)
    experience_years=serializers.IntegerField(allow_null=True)
    statement=serializers.CharField(allow_null=True)

    def create(self, validated_data):
        """
        Crea y guarda una nueva instancia de CenterAdministrator.
        No se guarda en la base de datos porque no se va a usar el modelo en la base de datos   
        porque depende de otros modelos que si se guardan en la base de datos
        """
        user=validated_data.get('user')
        yoga_center=validated_data.get('yoga_center')
        center_administrator=CenterAdministrator(
            user=user,
            yoga_center=yoga_center,is_active_profile=validated_data.get('is_active_profile', True),
            photo_profile=validated_data.get('photo_profile'),
            role=validated_data.get('role'),
            experience_years=validated_data.get('experience_years'),
            statement=validated_data.get('statement')
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
            
        # Determinar si tiene un perfil activo para enviarlo al dashboard o a la configuración inicial
        if hasattr(self.user, 'centeradministrator') and getattr(self.user.centeradministrator, 'is_active_profile', False):
            data['redirect_url'] = '/center_administrator/dashboard/'
        else:
            data['redirect_url'] = '/center_administrator/dashboard/config/'
            
        return data
