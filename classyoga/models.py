from django.db import models

from centeryoga.models import YogaCenter
from instructor.models import Instructor
# Create your models here.
class ClassYoga(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    center = models.ForeignKey(YogaCenter, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    schedules = models.JSONField()
    photo = models.ImageField(upload_to='classyoga')
    at_creation = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    capacity_class=models.IntegerField()
    def __str__(self):
        return f'{self.name}'
    def to_decrease_capacity(self):
        self.capacity_class=self.capacity_class-1
        self.save()
    def initialize_capacity(self,capacity:int):
        self.capacity_class=capacity
        self.save()