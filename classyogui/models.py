from django.db import models

from classyoga.models import ClassYoga
from yogui.models import Yogui
# Create your models here.
class ClassYogui(models.Model):
    class_yoga = models.ForeignKey(ClassYoga, on_delete=models.CASCADE)
    yogui = models.ForeignKey(Yogui, on_delete=models.CASCADE)
    at_creation = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['class_yoga', 'yogui'],
                                    name='unique_class_yogui')
        ]
    def __str__(self):
        return f'{self.class_yoga} - {self.yogui}'
