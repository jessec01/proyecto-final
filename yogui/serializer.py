from rest_framework import serializers
from .models import Yogui
import re
class YoguiSerializer(serializers.ModelSerializer):
    is_yogui = serializers.BooleanField(default=True,write_only=True)
    is_instructor = serializers.BooleanField(default=False,write_only=True)
    is_center_administrator = serializers.BooleanField(default=False,write_only=True)
    class Meta:
        model = Yogui
        fields = ['user','at_creation','photo_profile','description'] 
        read_only_fields = ['user','at_creation']
    def validate_description(self,value_description):
        description=re.search(r'^[a-zA-Z\s]{4,500}$',value_description)
        if not description:
            raise serializers.ValidationError({"description": "invalid description"})
        return value_description
    def validate_photo_profile(self, value_photo_profile):
        if value_photo_profile and not value_photo_profile.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError({"photo_profile": "Invalid file type. Only .jpg, .jpeg, and .png are allowed."})
        return value_photo_profile    
    def create(self, validated_data):
        user=validated_data.get('user')
        description=validated_data.get('description')
        photo_profile=validated_data.get('photo_profile')
        is_yogui=validated_data.get('is_yogui', True)
        is_instructor=validated_data.get('is_instructor', False)
        is_center_administrator=validated_data.get('is_center_administrator', False)

        yogui=Yogui.objects.create(
            user=user,
            description=description,
            photo_profile=photo_profile,
            is_yogui=is_yogui,
            is_instructor=is_instructor,
            is_center_administrator=is_center_administrator
        )
        return yogui

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
    