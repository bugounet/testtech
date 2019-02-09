# Generated by Django 2.1.5 on 2019-02-09 12:28

import api.models.training_configuration
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_trainingtask_docker_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingconfiguration',
            name='algorithm',
            field=models.FileField(blank=True, help_text='Submitted python algorithm', null=True, upload_to=api.models.training_configuration.get_algorithm_path),
        ),
        migrations.AlterField(
            model_name='trainingconfiguration',
            name='dockerfile',
            field=models.FileField(blank=True, help_text='Submitted dockerfile', null=True, upload_to=api.models.training_configuration.get_algorithm_path),
        ),
    ]