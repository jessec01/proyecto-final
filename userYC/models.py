
from  django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .manager import ManagerCustom
# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=30, unique=True,null=False,blank=False)
    email = models.EmailField(unique=True,max_length=250)

    first_name = models.CharField(max_length=30)
    last_name=models.CharField(null=False,blank=False,max_length=30)
    phone = PhoneNumberField(blank=False,null=False,unique=True,help_text='Contact phone number',region='VE')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_center_administrator = models.BooleanField(default=False)    
    is_instructor = models.BooleanField(default=False)
    is_yogui = models.BooleanField(default=False)
    objects = ManagerCustom()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'username']
    def __str__(self):
        return self.email
    def activate_user(self):
        self.is_active = True
        self.save()
    def deactivate_user(self):
        self.is_active = False
        self.save()
    