from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    date = models.DateField(default=timezone.now().date())
    time=models.TimeField(auto_now_add=True)
                                 #auto_now_add=True
    def __str__(self):
        return self.title

# Create your models here.
