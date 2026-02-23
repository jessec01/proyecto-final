#instrcutor/serializer.py
# importaciones estandar de python
import re 

# importaciones de terceros
from django.db import transaction
from rest_framework import serializers

# importaciones de models
from instructor.models import Instructor
from user.models import User    
class InstructorSerializer(serializers.ModelSerializer):
    """Serializer para crear un instructor"""
    class Meta:
        model = Instructor
        fields = ['user','at_creation','especiality','photo_profile','description'] 
    def validate_especiality(self,value_especiality):
        especiality=re.search('^[a-zA-Z\s]{4,100}$',value_especiality)
        if not especiality:
            raise serializers.ValidationError({"especiality": "invalid especiality"})
        return value_especiality
    def validate_description(self,value_description):
        description=re.search('^[a-zA-Z\s]{4,500}$',value_description)
        if not description:
            raise serializers.ValidationError({"description": "invalid description"})
        return value_description
    def validate_photo_profile(self, value_photo_profile):
        if value_photo_profile and not value_photo_profile.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError({"photo_profile": "Invalid file type. Only .jpg, .jpeg, and .png are allowed."})
        return value_photo_profile    
    def create(self, validated_data):
        user=validated_data.get('user')
        especiality=validated_data.get('especiality')
        description=validated_data.get('description')
        photo_profile=validated_data.get('photo_profile')
        #valida internamente el user.required
        with transaction.atomic():
            instructor=Instructor.objects.create(
                user=user,
                especiality=especiality,
                description=description,
                photo_profile=photo_profile
        )
        return instructor
class InstructorUpdateSerializer(serializers.ModelSerializer):
    """ Serializer para actualizar un instructor """
    class Meta:
        model = Instructor
        fields = ['especiality','photo_profile','description'] 
    def validate_especiality(self,value_especiality):
        especiality=re.search('^[a-zA-Z\s]{4,100}$',value_especiality)
        if not especiality:
            raise serializers.ValidationError({"especiality": "invalid especiality"})
        return value_especiality
    def validate_description(self,value_description):
        description=re.search('^[a-zA-Z\s]{4,500}$',value_description)
        if not description:
            raise serializers.ValidationError({"description": "invalid description"})
        return value_description
    def validate_photo_profile(self, value_photo_profile):
        if value_photo_profile and not value_photo_profile.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError({"photo_profile": "Invalid file type. Only .jpg, .jpeg, and .png are allowed."})
        return value_photo_profile   
class InstructorListSerializer(serializers.ModelSerializer):
    """ Serializer para listar un instructor """
    first_name=serializers.CharField(source='user.first_name',read_only=True)
    last_name=serializers.CharField(source='user.last_name',read_only=True)
    class Meta:
        model=Instructor
        fields=['first_name','last_name','especiality','photo_profile','description']
class UserSerializer(serializers.ModelSerializer):
    """ Serializer para mostrar un usuario """
    class Meta:
        model=User
        fields=['first_name','last_name','email']

class DetailInstructorSerializer(serializers.ModelSerializer):
    """ Serializer para mostrar un instructor """
    user=UserSerializer(read_only=True)
    class Meta:
        model=Instructor
        fields=['user','especiality','photo_profile','description']
class LoginSerializer(serializers.Serializer):
    """ Serializer para iniciar sesión """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)   
    def validate_email(self, value):
        email=re.search('^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$',value)
        if not email:
            raise serializers.ValidationError({"email": "invalid email"})
        return value
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError({"password": "Password is required."})
        return value
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"email": "Invalid email or password."})
        return attrs      
    