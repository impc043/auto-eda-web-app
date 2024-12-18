from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, null=True,blank=True)
    profile_img = models.ImageField(null=True, blank=True, upload_to='profile_img')
    

    def __str__(self):
        return str(self.user.username)
