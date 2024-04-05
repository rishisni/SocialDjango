from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    bio = models.CharField(max_length=400, blank=True) 
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

