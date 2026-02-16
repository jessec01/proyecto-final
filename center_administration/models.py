from django.db import models
from userYC.models import User
from centeryoga.models import YogaCenter
# Create your models here.
class CenterAdministrator(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    yoga_center=models.OneToOneField(YogaCenter, on_delete=models.CASCADE)
    is_active_profile=models.BooleanField(default=False)
    at_creation=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    def activate_profile(self):
        self.is_active_profile = True
        self.save()