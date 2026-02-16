
from django.contrib.auth.base_user import BaseUserManager
class ManagerCustom(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not extra_fields.get('first_name'):
            raise ValueError('El usuario debe tener un nombre')
        if not extra_fields.get('last_name'):
            raise ValueError('El usuario debe tener un apellido')
        if not extra_fields.get('phone'):
            raise ValueError('El usuario debe tener un número de teléfono')
        user=self.model(
           email=self.normalize_email(email),**extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True')
        user=self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user