from django.db import models

from userYC.models import User
from centeryoga.models import YogaCenter
# Create your models here.
class Instructor(models.Model):
    yogacenter=models.ForeignKey(YogaCenter,on_delete=models.CASCADE)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    at_creation=models.DateTimeField(auto_now_add=True)
    especiality=models.CharField(max_length=100)
    photo_profile=models.ImageField(upload_to='instructor_photos/', null=True, blank=True)
    description=models.TextField()
    def load_photo_profile(self, photo):
        self.photo_profile = photo
        self.save()
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'