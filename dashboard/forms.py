from .models import Project
from django.forms import ModelForm


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['user', 'created_date']