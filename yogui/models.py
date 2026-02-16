from django.db import models
from userYC.models import User
# Create your models here.
class Yogui(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    id_card=models.CharField(max_length=7, unique=True)
    photo_profile=models.ImageField(upload_to='yogui_photos/', null=True, blank=True)
    level_suscribed=models.CharField(max_length=20)
    at_creation=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    def load_photo_profile(self, photo):
        self.photo_profile = photo
        self.save()
    def update_level_suscribed(self, new_level):
        self.level_suscribed = new_level
        self.save()
    