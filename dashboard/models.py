from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    project_name = models.CharField(max_length=150, null=True,blank=True)
    project_file = models.FileField(null=True, blank=True, upload_to='csv_files')
    target_feature = models.CharField(max_length=100, null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.project_name)