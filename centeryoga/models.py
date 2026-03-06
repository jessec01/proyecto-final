from django.db import models
# Create your models here.
class YogaCenter(models.Model):
    
    code=models.CharField(max_length=10, unique=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=100)
    photo=models.ImageField(upload_to='static/img/', null=True, blank=True)
    description=models.TextField()
    capacity=models.IntegerField()
    active=models.BooleanField(default=True)
    hours_of_operation=models.JSONField()
    at_creation=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    def load_photo(self, photo):
        self.photo = photo
        self.save()

    def see_list_of_instructors(self):
        return self.instructor_set.all()
    def see_list_of_yoguis(self):
        return self.yogui_set.all()
   