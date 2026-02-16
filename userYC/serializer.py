import re
from rest_framework import serializers
from .models import User
from phonenumber_field.phonenumber import to_python
from django.db import transaction
class UserYCSerializer(serializers.ModelSerializer):
    confirmation_password = serializers.CharField(write_only=True)
    is_center_administrator = serializers.BooleanField(default=False,write_only=True)  
    is_instructor = serializers.BooleanField(default=False,write_only=True)
    is_yogui = serializers.BooleanField(default=False,write_only=True)
    class Meta:
        model = User    
        fields = ['username','email','first_name','last_name','phone','password','confirmation_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_username(self,value_username):
        if self.Meta.model.objects.filter(username=value_username).exists():
            raise serializers.ValidationError({"username": "username already exists"})
        
        usernameRegex = re.search('^(?=.*[a-zA-Z])(?!.*[#$<>])[a-zA-Z0-9_]{4,16}$',value_username)
        if not usernameRegex:
            raise serializers.ValidationError({"username": "invalid username"})
            pass
        return value_username 
    def validate_first_name(self,value_first_name):
        first_name=re.search('^[a-zA-Z]{4,16}$',value_first_name)
        if not first_name:
            raise serializers.ValidationError({"first name": "invalid name"})
        return value_first_name 
    def validate_last_name(self,value_last_name):
        last_name=re.search('^[a-zA-Z]{4,16}$',value_last_name)
        if not last_name:
            raise serializers.ValidationError({"last_name": "invalid last name"})
        return value_last_name 
    def validate_phone(self, value):
        value = to_python(value)
        if self.Meta.model.objects.filter(phone=value).exists():
            raise serializers.ValidationError({"phone":"phone number already exists."})
        
        if not value.is_valid():
            raise serializers.ValidationError({"phone":"Invalid phone number."}) 
        return value
    def validate_email(self,value_email):
        email=re.search('^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$',value_email)
        if not email:
            raise serializers.ValidationError({"email": "invalid email"})
        return value_email 
    def validate_password(self,value_password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:\'\"\\|,.<>\/?]).{8,16}$')
        if not pattern.match(value_password):
            raise serializers.ValidationError({'password': 'La contraseña debe tener 8-16 caracteres, al menos una mayúscula, un número y un símbolo.'})
        return value_password 
    def validate(self,attrs):
        password=attrs.get('password') 
        confirmation_password=attrs.get('confirmation_password')
        if password!=confirmation_password:
            
            raise serializers.ValidationError({"confirmation_password": "passwords do not match"})  
        return attrs 
    def create(self,validated_data):
        username=validated_data.get('username')
        email=validated_data.get('email')
        first_name=validated_data.get('first_name')     
        last_name=validated_data.get('last_name')
        phone=validated_data.get('phone')   
        password=validated_data.get('password')
        is_center_administrator=False
        is_instructor=False
        is_yogui=False
        if validated_data.get('is_center_administrator'):
            is_center_administrator=True
        elif validated_data.get('is_instructor'):
            is_instructor=True
        elif validated_data.get('is_yogui'):
            is_yogui=True

        with transaction.atomic():
            user=User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                password=password,
                is_center_administrator=is_center_administrator,
                is_instructor=is_instructor,
                is_yogui=is_yogui
            )
            user.activate_user()
            return user

