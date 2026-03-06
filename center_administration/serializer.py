#center_administration/serializer.py

#importaciones de python puro 
import re

#importaciones de rest_framework
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
#importaciones interna de center_administration
from centeryoga.models import YogaCenter
from centeryoga.serializer import YogaCenterSerializer
from classyoga.models import ClassYoga
from classyoga.serializer import ClassYogaSerializer
from classyogui.models import ClassYogui
from classyogui.serializer import ClassYoguiSerializer  
from .models import CenterAdministrator
from packages.models import Packages
from packages.serializer import PackagesSerializer
from policy.models import Policy
from policy.serializer import PolicySerializer
from promotion.models import Promotion
from promotion.serializer import PromotionSerializer
from rules.models import Rules
from rules.serializer import RulesSerializer
from userYC.models import User
from instructor.models import Instructor

#Serializador para el modelo CenterAdministrator
class CenterAdminSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo CenterAdministrator
    Se usa ModelSerializer en vez de Serializer porque se va a crear el modelo en la base de datos   
    Se usa para crear el perfil del administrador y para actualizarlo
    """
    class Meta:
        model=CenterAdministrator
        #todos los campos del modelo
        fields=['user','yoga_center','is_active_profile','photo_profile','role','experience_years','welcome_message']
        # Campos que no se pueden modificar
        read_only_fields=['user','yoga_center','is_active_profile','at_creation']
        def validate_photo_profile(self, value:str)->str:
            """validacion de url de foto correcta"""
            if value and not value.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise serializers.ValidationError({"photo_profile": "Invalid file type. Only .jpg, .jpeg, and .png are allowed."})
            return value 
        def validate_role(self, value:str)->str:
            """validacion de rol correcta"""
            if value and not re.match(r'^[a-zA-Z\s]{4,100}$', value):
                raise serializers.ValidationError({"role": "Invalid role"})
            return value 
        def validate_experience_years(self, value:int)->int:
            """validacion de experiencia correcta"""
            if value and not re.match(r'^[0-9]{1,2}$', str(value)):
                raise serializers.ValidationError({"experience_years": "Invalid experience years"})
            return value 
        def validate_welcome_message(self, value:str)->str:
            """validacion de mensaje de bienvenida correcta"""
            if value and not re.match(r'^[\w\s.,;:!¡?¿\'"áéíóúÁÉÍÓÚñÑüÜ()\-]{4,1000}$', value):
                raise serializers.ValidationError({"welcome_message": "El mensaje de bienvenida contiene caracteres no válidos o es muy largo/corto."})
            return value
        def create(self, validated_data:dict)->CenterAdministrator:
            """
            Crea y no guarda una nueva instancia de CenterAdministrator.
            """
            center_administrator=CenterAdministrator(**validated_data)
            return center_administrator
        def update(self, instance:CenterAdministrator, validated_data:dict)->CenterAdministrator:
            """
            Actualiza y no guarda una instancia de CenterAdministrator.
            """
            instance.user=validated_data.get('user',instance.user)
            instance.yoga_center=validated_data.get('yoga_center',instance.yoga_center)
            instance.is_active_profile=validated_data.get('is_active_profile',instance.is_active_profile)
            instance.photo_profile=validated_data.get('photo_profile',instance.photo_profile)
            instance.role=validated_data.get('role',instance.role)
            instance.experience_years=validated_data.get('experience_years',instance.experience_years)
            instance.welcome_message=validated_data.get('welcome_message',instance.welcome_message)
            return instance
class CenterDetailSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo CenterAdministrator
    Se usa ModelSerializer en vez de Serializer porque se va a crear el modelo en la base de datos   
    Se usa para crear el perfil del administrador
    """
    class Meta:
        model=CenterAdministrator
        #todos los campos del modelo
        fields=['user','yoga_center','is_active_profile','photo_profile','role','experience_years','welcome_message']
        # Campos que no se pueden modificar
        read_only_fields=['user','yoga_center','is_active_profile']
    def to_representation(self, instance):
        """
        Convierte una instancia de CenterAdministrator a una representación de diccionario.
        """
        return {
            'user': instance.user,
            'yoga_center': instance.yoga_center,
            'is_active_profile': instance.is_active_profile,
            'photo_profile': instance.photo_profile,
            'role': instance.role,
            'experience_years': instance.experience_years,
            'welcome_message': instance.welcome_message
        }
class ListCenterAdministratorSerializer(serializers.ModelSerializer):
    """se usa para listar los administradores
    Serializador para el modelo CenterAdministrator
    Se usa ModelSerializer en vez de Serializer porque se va a crear el modelo en la base de datos   
    Se usa para crear el perfil del administrador
    """
    class Meta:
        model=CenterAdministrator
        #todos los campos del modelo
        fields=['user','yoga_center','is_active_profile','photo_profile','role','experience_years','welcome_message']
        # Campos que no se pueden modificar
        read_only_fields=['user','yoga_center','is_active_profile']
    def to_representation(self, instance):
        """
        Convierte una instancia de CenterAdministrator a una representación de diccionario.
        """
        return {
            'user': instance.user,
            'yoga_center': instance.yoga_center,
            'is_active_profile': instance.is_active_profile,
            'photo_profile': instance.photo_profile,
            'role': instance.role,
            'experience_years': instance.experience_years,
            'welcome_message': instance.welcome_message
        }
class CenterAdministratorSerializer(serializers.Serializer):
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
    welcome_message=serializers.CharField(allow_null=True, required=False)

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
            welcome_message=validated_data.get('welcome_message')
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

class ClassYogaInitialSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    schedules = serializers.JSONField()
    category = serializers.CharField(max_length=100)

class CenterAdminConfiginitialSerializer(serializers.Serializer):
    """
        Maneja la transacion de la configuracion inicial del administrador del 
        centro, y los modelos dependiente a el.
    """
    center_administrator=CenterAdminSerializer()
    center=YogaCenterSerializer()
    rules=RulesSerializer()
    packages=PackagesSerializer()
    policy=PolicySerializer()
    promotion=PromotionSerializer()
    classyoga=ClassYogaInitialSerializer()
    def create(self, validated_data):
        #extraccion de la informacion de las reglas y del administrador del centro para crear las instancias correspondientes antes de crear el centro de yoga, esto se hace para asegurar la integridad de los datos y las relaciones entre las diferentes entidades del sistema.
        user=validated_data.pop('user')
        center=validated_data.pop('center')
        center_admin_data = validated_data.pop('center_administrator')
        rules_data = validated_data.pop('rules')
        packages_data = validated_data.pop('packages')
        promotion_data = validated_data.pop('promotion')
        policy_data = validated_data.pop('policy')
        classyoga_data = validated_data.pop('classyoga')
        #creacion de los modelos dependientes antes de crear el centro de yoga
        with transaction.atomic():           
            #orden de la transaccion 
            #1 yoga center
            #2 center administrator
            #3 instructor base
            #4 rules
            #5 packages
            #6 promotion
            #7 policy
            #8 classyoga
            #yoga center
            yoga_center=YogaCenter.objects.create(**center)
            #center administrator
            center_administrator:CenterAdministrator=CenterAdministrator.objects.create(user=user, yoga_center=yoga_center, **center_admin_data)
            #instructor base (para la clase)
            instructor_base = Instructor.objects.create(user=user, yogacenter=yoga_center, especiality='General', description='Instructor Inicial')
            #rules
            rules:Rules=Rules.objects.create(center=yoga_center, **rules_data)
            #packages
            packages:Packages=Packages.objects.create(center=yoga_center, **packages_data)
            #promotion
            promotion:Promotion=Promotion.objects.create(center=yoga_center, **promotion_data)
            #policy
            policy:Policy=Policy.objects.create(center=yoga_center, **policy_data)
            #classyoga
            classyoga:ClassYoga=ClassYoga.objects.create(center=yoga_center, instructor=instructor_base, **classyoga_data)
            #modificar el estado center para que se active una vez que se hayan creado todas las entidades relacionadas                                                
            center_administrator.activate_profile()
        return center_administrator


    
    