# Generated by Django 4.1.5 on 2023-03-21 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_project_project_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
